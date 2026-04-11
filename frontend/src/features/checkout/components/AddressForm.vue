<script setup lang="ts">
import { useForm } from 'vee-validate'
import { toTypedSchema } from '@vee-validate/zod'
import { z } from 'zod'

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

const schema = toTypedSchema(
  z.object({
    firstName: z.string().min(1, 'Required'),
    lastName:  z.string().min(1, 'Required'),
    address1:  z.string().min(1, 'Required'),
    address2:  z.string().optional().default(''),
    city:      z.string().min(1, 'Required'),
    state:     z.string().min(1, 'Required'),
    zip:       z.string().min(4, 'Invalid ZIP'),
    country:   z.string().default('MX'),
    phone:     z.string().min(8, 'Invalid phone'),
  })
)

const { handleSubmit, defineField, errors } = useForm({ validationSchema: schema })

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

    <div class="space-y-1">
      <label class="block text-[length:var(--text-micro)] uppercase tracking-[var(--tracking-label)]">Address</label>
      <input
        v-model="address1"
        v-bind="address1Attrs"
        type="text"
        autocomplete="address-line1"
        placeholder="Street address"
        class="w-full border border-[color:var(--color-border)] bg-transparent px-3 py-2.5 text-[length:var(--text-small)] focus:outline-none focus:border-[color:var(--color-obsidian)] transition-colors duration-[var(--duration-fast)]"
        :class="{ 'border-red-500': errors.address1 }"
      />
      <p v-if="errors.address1" class="text-[length:var(--text-micro)] text-red-600">{{ errors.address1 }}</p>
    </div>

    <div class="space-y-1">
      <input
        v-model="address2"
        v-bind="address2Attrs"
        type="text"
        autocomplete="address-line2"
        placeholder="Apt, suite, unit (optional)"
        class="w-full border border-[color:var(--color-border)] bg-transparent px-3 py-2.5 text-[length:var(--text-small)] focus:outline-none focus:border-[color:var(--color-obsidian)] transition-colors duration-[var(--duration-fast)]"
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
        <label class="block text-[length:var(--text-micro)] uppercase tracking-[var(--tracking-label)]">State</label>
        <input
          v-model="state"
          v-bind="stateAttrs"
          type="text"
          autocomplete="address-level1"
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
        <input
          v-model="phone"
          v-bind="phoneAttrs"
          type="tel"
          autocomplete="tel"
          class="w-full border border-[color:var(--color-border)] bg-transparent px-3 py-2.5 text-[length:var(--text-small)] focus:outline-none focus:border-[color:var(--color-obsidian)] transition-colors duration-[var(--duration-fast)]"
          :class="{ 'border-red-500': errors.phone }"
        />
        <p v-if="errors.phone" class="text-[length:var(--text-micro)] text-red-600">{{ errors.phone }}</p>
      </div>
    </div>

    <!-- Hidden country field defaults to MX -->
    <input v-model="country" v-bind="countryAttrs" type="hidden" />

    <button
      type="submit"
      class="w-full py-4 bg-[color:var(--color-obsidian)] text-[color:var(--color-ivory)] text-[length:var(--text-small)] tracking-[var(--tracking-label)] uppercase hover:opacity-80 transition-opacity duration-[var(--duration-normal)] mt-2"
    >
      Continue to Shipping
    </button>
  </form>
</template>
