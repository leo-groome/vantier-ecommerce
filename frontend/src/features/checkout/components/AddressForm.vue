<script setup lang="ts">
import { useForm } from 'vee-validate'
import { toTypedSchema } from '@vee-validate/zod'
import { z } from 'zod'
import { VueTelInput } from 'vue-tel-input'
import 'vue-tel-input/vue-tel-input.css'

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
}

const countries = [
  { code: 'US', name: 'United States' },
  { code: 'MX', name: 'Mexico' },
  { code: 'CA', name: 'Canada' },
  { code: 'GB', name: 'United Kingdom' },
  { code: 'AU', name: 'Australia' },
  { code: 'FR', name: 'France' },
  { code: 'DE', name: 'Germany' },
  { code: 'IT', name: 'Italy' },
  { code: 'ES', name: 'Spain' },
  { code: 'NL', name: 'Netherlands' },
  { code: 'JP', name: 'Japan' }
]

const schema = toTypedSchema(
  z.object({
    firstName: z.string().min(1, 'Required'),
    lastName:  z.string().min(1, 'Required'),
    address1:  z.string().min(3, 'Please provide street and number'),
    address2:  z.string().optional().default(''),
    city:      z.string().min(1, 'Required'),
    state:     z.string().min(1, 'State/Province is required'),
    zip:       z.string().min(3, 'Invalid ZIP / Postal Code'),
    country:   z.string().min(2, 'Please select a country'),
    phone:     z.string().regex(/^\+\d{7,15}$/, 'Must start with + and country code (e.g. +52 o +1)'),
  })
)

const { handleSubmit, defineField, errors } = useForm({ validationSchema: schema, initialValues: { country: 'US' } })

const [firstName, firstNameAttrs] = defineField('firstName')
const [lastName,  lastNameAttrs]  = defineField('lastName')
const [address1,  address1Attrs]  = defineField('address1')
const [address2,  address2Attrs]  = defineField('address2')
const [city,      cityAttrs]      = defineField('city')
const [state,     stateAttrs]     = defineField('state')
const [zip,       zipAttrs]       = defineField('zip')
const [country,   countryAttrs]   = defineField('country')
const [phone,     phoneAttrs]     = defineField('phone')

const onSubmit = handleSubmit((values) => emit('submit', values as AddressData))
</script>

<template>
  <form class="space-y-4" @submit.prevent="onSubmit">
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

    <!-- Country Dropdown -->
    <div class="space-y-1 relative">
      <label class="block text-[length:var(--text-micro)] uppercase tracking-[var(--tracking-label)]">Country / Region</label>
      <select
        v-model="country"
        v-bind="countryAttrs"
        autocomplete="country"
        class="w-full border border-[color:var(--color-border)] bg-transparent px-3 py-2.5 text-[length:var(--text-small)] focus:outline-none focus:border-[color:var(--color-obsidian)] transition-colors duration-[var(--duration-fast)] appearance-none rounded-none"
        :class="{ 'border-red-500': errors.country }"
      >
        <option value="" disabled>Select Country</option>
        <option v-for="c in countries" :key="c.code" :value="c.code">{{ c.name }}</option>
      </select>
      <div class="pointer-events-none absolute bottom-0 right-0 flex items-center px-3 pb-3 text-[color:var(--color-obsidian)]">
         <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path></svg>
      </div>
      <p v-if="errors.country" class="text-[length:var(--text-micro)] text-red-600">{{ errors.country }}</p>
    </div>

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

    <div class="space-y-1">
      <label class="block text-[length:var(--text-micro)] uppercase tracking-[var(--tracking-label)]">Apartment, suite, etc. (optional)</label>
      <input
        v-model="address2"
        v-bind="address2Attrs"
        type="text"
        autocomplete="address-line2"
        placeholder="Apt, Suite, Unit, Building, etc."
        class="w-full border border-[color:var(--color-border)] bg-transparent px-3 py-2.5 text-[length:var(--text-small)] focus:outline-none focus:border-[color:var(--color-obsidian)] transition-colors duration-[var(--duration-fast)]"
        :class="{ 'border-red-500': errors.address2 }"
      />
    </div>

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
        <label class="block text-[length:var(--text-micro)] uppercase tracking-[var(--tracking-label)]">Phone</label>
        <vue-tel-input
          v-model="phone"
          mode="international"
          :inputOptions="{ placeholder: 'Include country code (+1...)', autocomplete: 'tel' }"
          class="vantier-tel-input"
          :class="{ 'border-red-500': errors.phone }"
        />
        <p v-if="errors.phone" class="text-[length:var(--text-micro)] text-red-600">{{ errors.phone }}</p>
      </div>
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
/* Vantier minimal theme overrides for vue-tel-input */
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
  padding: 0.625rem 0.75rem; /* ~ py-2.5 px-3 */
  font-size: var(--text-small);
  font-family: inherit;
  color: var(--color-on-surface);
}
:deep(.vti__input::placeholder) {
  color: #9ca3af; /* fallback gray */
}
:deep(.vti__dropdown) {
  padding: 0 0.75rem;
  background: transparent;
  border-radius: 0;
  transition: background-color var(--duration-fast);
}
:deep(.vti__dropdown:hover) {
  background: var(--color-warm-beige);
}
/* Dropdown List Styling */
:deep(.vti__dropdown-list) {
  border: 1px solid var(--color-border) !important;
  border-radius: 0 !important;
  box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.1) !important;
  margin-top: 4px;
  background-color: var(--color-ivory) !important;
  width: 340px !important; /* Fixed width to prevent ugly wrapping */
  max-height: 250px !important;
  font-family: inherit !important;
  text-align: left;
  z-index: 50; /* Ensure it floats above the button */
}
/* Scrollbar for the dropdown */
:deep(.vti__dropdown-list::-webkit-scrollbar) {
  width: 4px;
}
:deep(.vti__dropdown-list::-webkit-scrollbar-thumb) {
  background-color: var(--color-border-strong);
}
/* Dropdown Items */
:deep(.vti__dropdown-item) {
  padding: 10px 14px !important;
  font-size: var(--text-small) !important;
  color: var(--color-on-surface) !important;
  transition: background-color var(--duration-fast);
}
/* Strip bold from country names */
:deep(.vti__dropdown-item strong) {
  font-weight: 400 !important;
}
:deep(.vti__dropdown-item.highlighted) {
  background-color: var(--color-warm-beige) !important;
}
:deep(.border-red-500) {
  border-color: #ef4444 !important;
}
</style>
