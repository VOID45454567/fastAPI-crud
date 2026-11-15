import type { Axios } from "axios";
import { AxiosError } from "axios";
import type { ApiErrorBody, ApiResponse } from "@/types/ApiResponse";
import type { Task } from "@/types/Task";



function toDateString(d: Date): string {
    const y = d.getFullYear();
    const m = String(d.getMonth() + 1).padStart(2, "0");
    const day = String(d.getDate()).padStart(2, "0");
    return `${y}-${m}-${day}`;
}

export class TasksApi {
    constructor(
        private readonly api: Axios,
        private readonly baseUrl: string,
    ) { }

    private handleError(err: unknown): { success: false; error: string; status?: number } {
        const error = err as AxiosError<ApiErrorBody>;

        if (error.response) {
            const { status, data } = error.response;
            const detail = data?.detail;

            let message = "Ошибка сервера";
            if (typeof detail === "string") {
                message = detail;
            } else if (Array.isArray(detail)) {
                message = detail.map((d) => d.msg).join("; ");
            }
            return { success: false, error: message, status };
        }

        if (error.request) return { success: false, error: "Нет ответа от сервера" };
        return { success: false, error: error.message };
    }

    async create(
        userId: number,
        title: string,
        description: string,
        status: string,
        priority: number,
        due_date: Date,
    ): Promise<ApiResponse<Task>> {
        try {
            const response = await this.api.post<Task>(
                `${this.baseUrl}/tasks`,
                {
                    title,
                    description,
                    status,
                    priority,
                    due_date: toDateString(due_date),
                },
                { params: { user_id: userId } },
            );
            return { success: true, data: response.data, status: response.status };
        } catch (err) {
            return this.handleError(err);
        }
    }

    async getAll(params?: {
        userId?: number;
        status?: string;
        skip?: number;
        limit?: number;
    }): Promise<ApiResponse<Task[]>> {
        try {
            const query: Record<string, string | number> = {};
            if (params?.userId !== undefined) query.user_id = params.userId;
            if (params?.status !== undefined) query.status = params.status;
            if (params?.skip !== undefined) query.skip = params.skip;
            if (params?.limit !== undefined) query.limit = params.limit;

            const response = await this.api.get<Task[]>(`${this.baseUrl}/tasks`, {
                params: query,
            });
            return { success: true, data: response.data, status: response.status };
        } catch (err) {
            return this.handleError(err);
        }
    }

    async getOne(id: number): Promise<ApiResponse<Task>> {
        try {
            const response = await this.api.get<Task>(`${this.baseUrl}/tasks/${id}`);
            return { success: true, data: response.data, status: response.status };
        } catch (err) {
            return this.handleError(err);
        }
    }

    async getByUserId(userId: number): Promise<ApiResponse<Task[]>> {
        try {
            const response = await this.api.get<Task[]>(
                `${this.baseUrl}/users/${userId}/tasks`,
            );
            return { success: true, data: response.data, status: response.status };
        } catch (err) {
            return this.handleError(err);
        }
    }

    async delete(id: number): Promise<ApiResponse<null>> {
        try {
            const response = await this.api.delete(`${this.baseUrl}/tasks/${id}`);
            return { success: true, data: null, status: response.status };
        } catch (err) {
            return this.handleError(err);
        }
    }
}