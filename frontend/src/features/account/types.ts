export interface SavedAddress {
  id: string
  street: string
  city: string
  state: string
  zip: string
  country: string
  isDefault: boolean
}

export interface User {
  id: string
  email: string
  name: string
  role: 'customer' | 'Owner' | 'Operative'
}
