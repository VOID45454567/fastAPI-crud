import { defineStore } from "pinia";
import { ref } from "vue";

import { api } from "@/api";
import { TasksApi } from "@/api/tasks";
import { useAuthStore } from "@/stores/auth";
import type { Task } from "@/types/Task";

export const useTasksStore = defineStore("tasks", () => {
    const tasksApi = new TasksApi(api, import.meta.env.VITE_BASE_URL);
    const authStore = useAuthStore();

    const allTasks = ref<Task[]>([]);
    const myTasks = ref<Task[]>([]);
    const loading = ref(false);
    const error = ref<string | null>(null);

    const getAllTasks = async (): Promise<void> => {
        loading.value = true;
        error.value = null;

        const result = await tasksApi.getAll();

        loading.value = false;
        if (result.success) {
            allTasks.value = result.data;
        } else {
            error.value = result.error;
        }
    };

    const getMyTasks = async (): Promise<void> => {
        const userId = authStore.currentUser?.id;
        if (!userId) {
            error.value = "Пользователь не авторизован";
            return;
        }

        loading.value = true;
        error.value = null;

        const result = await tasksApi.getByUserId(userId);

        loading.value = false;
        if (result.success) {
            myTasks.value = result.data;
        } else {
            error.value = result.error;
        }
    };

    const createTask = async (
        title: string,
        description: string,
        status: string,
        priority: number,
        due_date: Date,
    ): Promise<void> => {
        const userId = authStore.currentUser?.id;
        if (!userId) {
            error.value = "Пользователь не авторизован";
            return;
        }

        loading.value = true;
        error.value = null;

        const result = await tasksApi.create(
            userId,
            title,
            description,
            status,
            priority,
            due_date,
        );

        loading.value = false;
        if (result.success) {
            myTasks.value.push(result.data);
            allTasks.value.push(result.data);
        } else {
            error.value = result.error;
        }
    };

    const deleteTask = async (id: number): Promise<void> => {
        loading.value = true;
        error.value = null;

        const result = await tasksApi.delete(id);

        loading.value = false;
        if (result.success) {
            myTasks.value = myTasks.value.filter((t) => t.id !== id);
            allTasks.value = allTasks.value.filter((t) => t.id !== id);
        } else {
            error.value = result.error;
        }
    };

    return {
        allTasks,
        myTasks,
        loading,
        error,
        getAllTasks,
        getMyTasks,
        createTask,
        deleteTask,
    };
});