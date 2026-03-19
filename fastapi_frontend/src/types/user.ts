export type UUID = string
export type ISODateString = string
export type EmailString = string

export type Token = {
  access_token: string
  token_type: "bearer" | string
}

export type UserBase = {
  email: EmailString
  is_active: boolean
  is_superuser: boolean
  full_name: string | null
}

export type AccessToken = {
  username: string
  password: string
}

export type UserCreate = UserBase & {
  password: string
}

export type UserUpdate = {
  password?: string | null
  email?: EmailString | null
}

export type User = UserBase & {
  id: UUID
  hashed_password: string
  created_at: ISODateString | null
}

export type UserPublic = UserBase & {
  id: UUID
  created_at: ISODateString | null
}

export type UserUpdateMe = {
  full_name?: string | null
  email?: EmailString | null
}

export type UserInDB = {
  data: UserPublic[]
  count: number
}

export type UserRegister = {
  email: EmailString
  password: string
  full_name: string | null
}

export type TokenPayload = {
  sub: string | null
}

export type NewPassword = {
  token: string
  new_password: string
}

export type Message = {
  message: string
}