import { api } from "@/api";
import { AuthApi } from "@/api/auth";
import router from "@/router";
import type { User } from "@/types/User";
import { defineStore } from "pinia";
import { ref } from "vue";

export const useAuthStore = defineStore('auth', () => {

    const authApi = new AuthApi(
        api,
        import.meta.env.VITE_BASE_URL
    )

    const isAutheficated = ref<boolean>(false)
    const currentUser = ref<User | null>(null)

    const register = async (login: string, email: string) => {
        console.log(import.meta.env.VITE_BASE_URL);

        const responce = await authApi.register(login, email)

        if (responce.success) {
            setCurrentUser(responce.data)
            setIsAuth(true)

            localStorage.setItem("id", String(currentUser.value!.id))

            router.push({
                name: 'dashboard'
            })
        }
    }

    const setIsAuth = (auth: boolean): void => {
        isAutheficated.value = auth
    }

    const getMe = async () => {
        const id = ref<number | null>(Number(localStorage.getItem("id")))

        if (id === null) {
            setIsAuth(false)
            setCurrentUser(null)
            router.push({
                name: 'register'
            })

        }

        const responce = await authApi.getMe(id.value!)

        if (responce.success) {
            setIsAuth(true)
            setCurrentUser(responce.data)
        }
    }

    const setCurrentUser = (user: User | null) => {
        currentUser.value = user
    }


    return {
        isAutheficated,
        currentUser,

        register,
        getMe
    }

})