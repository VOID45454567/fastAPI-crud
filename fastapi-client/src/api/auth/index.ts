import type { ApiResponse, ApiErrorBody } from "@/types/ApiResponse"
import type { User } from "@/types/User"
import type { Axios, AxiosError } from "axios"

export class AuthApi {

    constructor(
        private readonly api: Axios,
        private readonly baseUrl: string
    ) { }

    async register(login: string, email: string): Promise<ApiResponse<User>> {
        try {
            const response = await this.api.post<User>(
                `${this.baseUrl}/users`,
                { login, email },
            )
            return { success: true, data: response.data, status: response.status }
        } catch (err) {
            const error = err as AxiosError<ApiErrorBody>

            if (error.response) {
                const { status, data } = error.response
                const detail = data?.detail

                let message = 'Ошибка сервера'

                if (typeof detail === 'string') {
                    message = detail
                } else if (Array.isArray(detail)) {
                    message = detail.map((d) => d.msg).join('; ')
                }

                return { success: false, error: message, status }
            }

            if (error.request) {
                return { success: false, error: 'Нет ответа от сервера' }
            }

            return { success: false, error: error.message }
        }
    }


    async getMe(id: number): Promise<ApiResponse<User>> {
        try {
            const response = await this.api.get<User>(`${this.baseUrl}/users/${id}`)
            return { success: true, data: response.data, status: response.status }
        } catch (err) {
            const error = err as AxiosError<ApiErrorBody>

            if (error.response) {
                const { status, data } = error.response
                const detail = data?.detail

                let message = 'Ошибка сервера'

                if (typeof detail === 'string') {
                    message = detail
                } else if (Array.isArray(detail)) {
                    message = detail.map((d) => d.msg).join('; ')
                }

                return { success: false, error: message, status }
            }

            if (error.request) {
                return { success: false, error: 'Нет ответа от сервера' }
            }

            return { success: false, error: error.message }
        }
    }
}