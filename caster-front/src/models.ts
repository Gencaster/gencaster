export enum UserDataRequestType {
  Gps = "gps",
  String = "string",
}

export interface UserDataRequest {
  name: string;
  description: string;
  key: string;
  type: UserDataRequestType;
  placeholder: string;
}

export enum PlayerState {
  Start = "start",
  Playing = "playing",
  End = "end",
}

export enum DrifterStatus {
  WaitForStart = "waitForStart",
  WaitForUserInput = "waitForUserInput",
  DisplayPlayer = "displayPlayer",
  ShowEndScreen = "showEndScreen",
}
