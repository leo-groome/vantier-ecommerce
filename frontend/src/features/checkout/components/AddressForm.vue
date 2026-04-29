<script setup lang="ts">
import { nextTick, onMounted, ref, markRaw } from 'vue'
import { useForm } from 'vee-validate'
import { toTypedSchema } from '@vee-validate/zod'
import { z } from 'zod'
import { VueTelInput } from 'vue-tel-input'
import 'vue-tel-input/vue-tel-input.css'
import { setOptions, importLibrary } from '@googlemaps/js-api-loader'

const emit = defineEmits<{ (e: 'submit', data: AddressData): void }>()

export interface AddressData {
  firstName: string
  lastName: string
  address1: string
  address2: string
  city: string
  state: string
  zip: string
  country: string
  phone: string
  district: string
}

const schema = toTypedSchema(
  z.object({
    firstName: z.string().min(1, 'Required'),
    lastName:  z.string().min(1, 'Required'),
    address1:  z.string().min(3, 'Please provide street and number'),
    address2:  z.string().optional().default(''),
    city:      z.string().min(1, 'Required'),
    state:     z.string().optional().default(''),
    zip:       z.string().min(3, 'Invalid ZIP / Postal Code'),
    country:   z.string().min(2, 'Required'),
    phone:     z.string().regex(/^\+[\d\s-]{7,20}$/, 'Must start with + and country code (e.g. +52 or +1)'),
    district:  z.string().optional().default(''),
  })
)

const { handleSubmit, defineField, errors, setFieldValue } = useForm({
  validationSchema: schema,
  initialValues: { country: '' },
})

const [firstName, firstNameAttrs] = defineField('firstName')
const [lastName,  lastNameAttrs]  = defineField('lastName')
const [address1,  address1Attrs]  = defineField('address1')
const [address2,  address2Attrs]  = defineField('address2')
const [city,      cityAttrs]      = defineField('city')
const [state,     stateAttrs]     = defineField('state')
const [zip,       zipAttrs]       = defineField('zip')
const [country,   countryAttrs]   = defineField('country')
const [phone,     phoneAttrs]     = defineField('phone')
const [district,  districtAttrs]  = defineField('district')

const searchQuery = ref('')
const predictions = ref<any[]>([])
let AutocompleteSuggestionClass: any = null

const autocompleteReady = ref(false)
const placesError = ref('')

function getComp(
  comps: any[],
  type: string,
  nameType: 'longText' | 'shortText' = 'longText',
): string {
  return comps.find((c: any) => c.types.includes(type))?.[nameType] ?? ''
}

onMounted(async () => {
  await nextTick()

  const apiKey = import.meta.env.VITE_GOOGLE_MAPS_API_KEY as string
  if (!apiKey) {
    placesError.value = 'VITE_GOOGLE_MAPS_API_KEY not set'
    return
  }

  try {
    setOptions({ key: apiKey, v: 'weekly' })
    const placesLib = await importLibrary('places') as any

    // Use the New Places API programmatically
    AutocompleteSuggestionClass = placesLib.AutocompleteSuggestion

    autocompleteReady.value = true
  } catch (err) {
    placesError.value = String(err)
    console.error('[AddressForm] Places API error:', err)
  }
})

async function onSearchInput() {
  if (!AutocompleteSuggestionClass || !searchQuery.value) {
    predictions.value = []
    return
  }
  try {
    const { suggestions } = await AutocompleteSuggestionClass.fetchAutocompleteSuggestions({
      input: searchQuery.value
    })
    // markRaw prevents Vue from proxying the Google Maps class instances
    predictions.value = (suggestions || []).map((s: any) => markRaw(s))
  } catch (err) {
    console.error('[AddressForm] fetchAutocompleteSuggestions error:', err)
    predictions.value = []
  }
}

async function selectPrediction(suggestion: any) {
  // suggestion.placePrediction.text.text contains the full description
  searchQuery.value = suggestion.placePrediction?.text?.text || ''
  predictions.value = []

  const place = suggestion.placePrediction?.toPlace()
  if (!place) return

  try {
    await place.fetchFields({ fields: ['addressComponents'] })
    
    const comps = place.addressComponents
    if (!comps) return

    // Street: number + route
    const streetNum = getComp(comps, 'street_number')
    const route     = getComp(comps, 'route')
    const street    = streetNum ? `${streetNum} ${route}` : route
    if (street) setFieldValue('address1', street)

    // City
    const cityVal =
      getComp(comps, 'locality') ||
      getComp(comps, 'sublocality_level_1') ||
      getComp(comps, 'administrative_area_level_2')
    if (cityVal) setFieldValue('city', cityVal)

    // State (short code: CA, AGS, CDMX…)
    const stateVal = getComp(comps, 'administrative_area_level_1', 'shortText')
    if (stateVal) setFieldValue('state', stateVal)

    // ZIP
    const zipVal = getComp(comps, 'postal_code')
    if (zipVal) setFieldValue('zip', zipVal)

    // Country (ISO2: MX, US, DE…)
    const countryCode = getComp(comps, 'country', 'shortText')
    if (countryCode) setFieldValue('country', countryCode.toUpperCase())

    // Colonia / District (Mexico — sublocality_level_1)
    const districtVal =
      getComp(comps, 'sublocality_level_1') ||
      getComp(comps, 'sublocality') ||
      getComp(comps, 'neighborhood')
    if (districtVal) setFieldValue('district', districtVal)

  } catch (err) {
    console.error('[AddressForm] fetchFields error:', err)
  }
}

const onSubmit = handleSubmit((values) => emit('submit', values as AddressData))
</script>

<template>
  <form class="space-y-5" @submit.prevent="onSubmit">

    <!-- Error banner (only visible when something goes wrong) -->
    <div
      v-if="placesError"
      class="text-xs text-amber-800 bg-amber-50 border border-amber-200 px-3 py-2"
    >
      Address search unavailable — fill in manually. ({{ placesError }})
    </div>

    <!-- Name -->
    <div class="grid grid-cols-2 gap-4">
      <div class="space-y-1">
        <label class="block text-[length:var(--text-micro)] uppercase tracking-[var(--tracking-label)]">First Name</label>
        <input
          v-model="firstName"
          v-bind="firstNameAttrs"
          type="text"
          autocomplete="given-name"
          class="w-full border border-[color:var(--color-border)] bg-transparent px-3 py-2.5 text-[length:var(--text-small)] focus:outline-none focus:border-[color:var(--color-obsidian)] transition-colors duration-[var(--duration-fast)]"
          :class="{ 'border-red-500': errors.firstName }"
        />
        <p v-if="errors.firstName" class="text-[length:var(--text-micro)] text-red-600">{{ errors.firstName }}</p>
      </div>
      <div class="space-y-1">
        <label class="block text-[length:var(--text-micro)] uppercase tracking-[var(--tracking-label)]">Last Name</label>
        <input
          v-model="lastName"
          v-bind="lastNameAttrs"
          type="text"
          autocomplete="family-name"
          class="w-full border border-[color:var(--color-border)] bg-transparent px-3 py-2.5 text-[length:var(--text-small)] focus:outline-none focus:border-[color:var(--color-obsidian)] transition-colors duration-[var(--duration-fast)]"
          :class="{ 'border-red-500': errors.lastName }"
        />
        <p v-if="errors.lastName" class="text-[length:var(--text-micro)] text-red-600">{{ errors.lastName }}</p>
      </div>
    </div>

    <!-- Custom Address Search with AutocompleteService -->
    <div class="space-y-1 relative">
      <label class="block text-[length:var(--text-micro)] uppercase tracking-[var(--tracking-label)]">
        Search Address
        <span v-if="autocompleteReady" class="ml-1 normal-case tracking-normal font-normal text-[color:var(--color-border-strong)]">
          · powered by Google — any country
        </span>
        <span v-else-if="!placesError" class="ml-1 normal-case tracking-normal font-normal text-[color:var(--color-border-strong)]">
          · loading…
        </span>
      </label>
      
      <input
        v-model="searchQuery"
        type="text"
        placeholder="Start typing your address…"
        class="w-full border border-[color:var(--color-border)] bg-transparent px-3 py-2.5 text-[length:var(--text-small)] focus:outline-none focus:border-[color:var(--color-obsidian)] transition-colors duration-[var(--duration-fast)]"
        @input="onSearchInput"
      />
      
      <!-- Custom Dropdown -->
      <ul v-if="predictions.length > 0" class="absolute z-50 w-full bg-[color:var(--color-ivory)] border border-[color:var(--color-border)] shadow-lg mt-1 max-h-60 overflow-y-auto">
        <li
          v-for="(suggestion, i) in predictions"
          :key="suggestion.placePrediction?.placeId || i"
          class="px-3 py-2 text-[length:var(--text-small)] hover:bg-[color:var(--color-warm-beige)] cursor-pointer border-b border-[color:var(--color-border)] last:border-0"
          @click="selectPrediction(suggestion)"
        >
          <div class="font-medium text-[color:var(--color-obsidian)]">{{ suggestion.placePrediction?.mainText?.text || suggestion.placePrediction?.text?.text }}</div>
          <div v-if="suggestion.placePrediction?.secondaryText?.text" class="text-[length:var(--text-micro)] text-gray-500">{{ suggestion.placePrediction.secondaryText.text }}</div>
        </li>
      </ul>
    </div>

    <!-- Street (auto-filled, editable) -->
    <div class="space-y-1">
      <label class="block text-[length:var(--text-micro)] uppercase tracking-[var(--tracking-label)]">Street Address</label>
      <input
        v-model="address1"
        v-bind="address1Attrs"
        type="text"
        autocomplete="address-line1"
        placeholder="Street name and number"
        class="w-full border border-[color:var(--color-border)] bg-transparent px-3 py-2.5 text-[length:var(--text-small)] focus:outline-none focus:border-[color:var(--color-obsidian)] transition-colors duration-[var(--duration-fast)]"
        :class="{ 'border-red-500': errors.address1 }"
      />
      <p v-if="errors.address1" class="text-[length:var(--text-micro)] text-red-600">{{ errors.address1 }}</p>
    </div>

    <!-- Apt / Suite -->
    <div class="space-y-1">
      <label class="block text-[length:var(--text-micro)] uppercase tracking-[var(--tracking-label)]">Apartment, suite, etc. (optional)</label>
      <input
        v-model="address2"
        v-bind="address2Attrs"
        type="text"
        autocomplete="address-line2"
        placeholder="Apt, Suite, Unit, Building…"
        class="w-full border border-[color:var(--color-border)] bg-transparent px-3 py-2.5 text-[length:var(--text-small)] focus:outline-none focus:border-[color:var(--color-obsidian)] transition-colors duration-[var(--duration-fast)]"
      />
    </div>

    <!-- City + State -->
    <div class="grid grid-cols-2 gap-4">
      <div class="space-y-1">
        <label class="block text-[length:var(--text-micro)] uppercase tracking-[var(--tracking-label)]">City</label>
        <input
          v-model="city"
          v-bind="cityAttrs"
          type="text"
          autocomplete="address-level2"
          class="w-full border border-[color:var(--color-border)] bg-transparent px-3 py-2.5 text-[length:var(--text-small)] focus:outline-none focus:border-[color:var(--color-obsidian)] transition-colors duration-[var(--duration-fast)]"
          :class="{ 'border-red-500': errors.city }"
        />
        <p v-if="errors.city" class="text-[length:var(--text-micro)] text-red-600">{{ errors.city }}</p>
      </div>
      <div class="space-y-1">
        <label class="block text-[length:var(--text-micro)] uppercase tracking-[var(--tracking-label)]">State / Province</label>
        <input
          v-model="state"
          v-bind="stateAttrs"
          type="text"
          autocomplete="address-level1"
          placeholder="State or Province"
          class="w-full border border-[color:var(--color-border)] bg-transparent px-3 py-2.5 text-[length:var(--text-small)] focus:outline-none focus:border-[color:var(--color-obsidian)] transition-colors duration-[var(--duration-fast)]"
          :class="{ 'border-red-500': errors.state }"
        />
        <p v-if="errors.state" class="text-[length:var(--text-micro)] text-red-600">{{ errors.state }}</p>
      </div>
    </div>

    <!-- Colonia — auto-shown for MX or when Google fills it -->
    <div v-if="country === 'MX' || district" class="space-y-1">
      <label class="block text-[length:var(--text-micro)] uppercase tracking-[var(--tracking-label)]">Colonia / Neighborhood</label>
      <input
        v-model="district"
        v-bind="districtAttrs"
        type="text"
        placeholder="e.g. Centro, Del Valle, Polanco"
        class="w-full border border-[color:var(--color-border)] bg-transparent px-3 py-2.5 text-[length:var(--text-small)] focus:outline-none focus:border-[color:var(--color-obsidian)] transition-colors duration-[var(--duration-fast)]"
      />
    </div>

    <!-- ZIP + Country -->
    <div class="grid grid-cols-2 gap-4">
      <div class="space-y-1">
        <label class="block text-[length:var(--text-micro)] uppercase tracking-[var(--tracking-label)]">ZIP / Postal Code</label>
        <input
          v-model="zip"
          v-bind="zipAttrs"
          type="text"
          autocomplete="postal-code"
          class="w-full border border-[color:var(--color-border)] bg-transparent px-3 py-2.5 text-[length:var(--text-small)] focus:outline-none focus:border-[color:var(--color-obsidian)] transition-colors duration-[var(--duration-fast)]"
          :class="{ 'border-red-500': errors.zip }"
        />
        <p v-if="errors.zip" class="text-[length:var(--text-micro)] text-red-600">{{ errors.zip }}</p>
      </div>
      <div class="space-y-1">
        <label class="block text-[length:var(--text-micro)] uppercase tracking-[var(--tracking-label)]">Country</label>
        <input
          v-model="country"
          v-bind="countryAttrs"
          type="text"
          autocomplete="country"
          placeholder="Auto-detected"
          class="w-full border border-[color:var(--color-border)] bg-transparent px-3 py-2.5 text-[length:var(--text-small)] focus:outline-none focus:border-[color:var(--color-obsidian)] transition-colors duration-[var(--duration-fast)] uppercase"
          :class="{ 'border-red-500': errors.country }"
        />
        <p v-if="errors.country" class="text-[length:var(--text-micro)] text-red-600">{{ errors.country }}</p>
      </div>
    </div>

    <!-- Phone -->
    <div class="space-y-1">
      <label class="block text-[length:var(--text-micro)] uppercase tracking-[var(--tracking-label)]">Phone</label>
      <vue-tel-input
        v-model="phone"
        mode="international"
        :inputOptions="{ placeholder: 'Include country code (+1, +52…)', autocomplete: 'tel' }"
        class="vantier-tel-input"
        :class="{ 'border-red-500': errors.phone }"
      />
      <p v-if="errors.phone" class="text-[length:var(--text-micro)] text-red-600">{{ errors.phone }}</p>
    </div>

    <button
      type="submit"
      class="w-full py-4 bg-[color:var(--color-obsidian)] text-[color:var(--color-ivory)] text-[length:var(--text-small)] tracking-[var(--tracking-label)] uppercase hover:opacity-80 transition-opacity duration-[var(--duration-normal)] mt-2"
    >
      Continue to Shipping
    </button>
  </form>
</template>

<style scoped>

/* vue-tel-input */
:deep(.vantier-tel-input) {
  border: 1px solid var(--color-border);
  border-radius: 0;
  background: transparent;
  box-shadow: none !important;
  font-family: inherit;
}
:deep(.vantier-tel-input:focus-within) {
  border-color: var(--color-obsidian);
  box-shadow: none !important;
}
:deep(.vti__input) {
  background: transparent;
  padding: 0.625rem 0.75rem;
  font-size: var(--text-small);
  font-family: inherit;
  color: var(--color-on-surface);
}
:deep(.vti__input::placeholder) { color: #9ca3af; }
:deep(.vti__dropdown) {
  padding: 0 0.75rem;
  background: transparent;
  border-radius: 0;
  transition: background-color var(--duration-fast);
}
:deep(.vti__dropdown:hover) { background: var(--color-warm-beige); }
:deep(.vti__dropdown-list) {
  border: 1px solid var(--color-border) !important;
  border-radius: 0 !important;
  box-shadow: 0 10px 30px -10px rgba(0,0,0,0.1) !important;
  margin-top: 4px;
  background-color: var(--color-ivory) !important;
  width: 340px !important;
  max-height: 250px !important;
  font-family: inherit !important;
  text-align: left;
  z-index: 50;
}
:deep(.vti__dropdown-list::-webkit-scrollbar) { width: 4px; }
:deep(.vti__dropdown-list::-webkit-scrollbar-thumb) { background-color: var(--color-border-strong); }
:deep(.vti__dropdown-item) {
  padding: 10px 14px !important;
  font-size: var(--text-small) !important;
  color: var(--color-on-surface) !important;
  transition: background-color var(--duration-fast);
}
:deep(.vti__dropdown-item strong) { font-weight: 400 !important; }
:deep(.vti__dropdown-item.highlighted) { background-color: var(--color-warm-beige) !important; }
:deep(.border-red-500) { border-color: #ef4444 !important; }

</style>
