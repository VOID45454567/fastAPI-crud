export type ApiResponse<T> =
    | { success: true; data: T; status: number }
    | { success: false; error: string; status?: number }

export interface ApiErrorBody {
    detail: string | { msg: string; loc: (string | number)[] }[]
}