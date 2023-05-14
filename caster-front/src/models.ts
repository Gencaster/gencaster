export type UserDataRequestType = "gps" | "string";
export interface UserDataRequest {
  name: string
  description: string
  key: string
  type: UserDataRequestType
  placeholder: string
}

export type PlayerState = "start" | "playing" | "end";
