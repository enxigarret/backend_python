
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import { useNavigate } from "@tanstack/react-router"
import {  UserPublic, UserRegister,AccessToken } from "../types/user"


const LoginService = {
    loginAccessToken: async ({formData}: {formData: AccessToken}) => {
        const response = await fetch("/api/auth/login", {
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded"
            },
            body: new URLSearchParams({
                username: formData.token,
                password: formData.type
            })
        })
        if (!response.ok) {
            throw new Error("Login failed")
        }
        return response.json()
    }
}

const UserService = {
    readUserMe: async (): Promise<UserPublic> => {
        const token = localStorage.getItem("token")
        if (!token) {
            throw new Error("No token found")
        }       const response = await fetch("/api/users/me", {     }
        )
        if (!response.ok) {
            throw new Error("Failed to fetch user data")
        }
        return response.json()
    },
    register: async ({requestBody}: {requestBody: UserRegister}) => {
        const response = await fetch("/api/auth/register", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(requestBody)
        })
        if (!response.ok) {
            throw new Error("Registration failed")
        }
        return response.json()
    }
}




const isLoggedIn = () => {
    return localStorage.getItem("token") !== null
}

const useAuth = () => {
    const navigate = useNavigate()
    const queryClient = useQueryClient()


    const { data: user} = useQuery<UserPublic | null ,Error>({
        queryKey: ["currentUser"],
        queryFn: UserService.readUserMe,
        enabled: isLoggedIn(),

    } )

    const signUpMutation = useMutation({
        mutationFn: (data:UserRegister)=> 
            UserService.register({requestBody: data}),
        onSuccess: () => {
            navigate({to:"/login"})
        },
        onError: ()=>{},
        onSettled: () => {
            queryClient.invalidateQueries({
                queryKey: ["currentUser"]
            })
        }
    })

    const login = async (data: AccessToken) => {
        const response= await LoginService.loginAccessToken({
            formData: data
        })
        localStorage.setItem("token", response.access_token)
        }

    const loginMutation = useMutation({
        mutationFn: login,
        onSuccess: () => {
            navigate({to:"/"})
        }
    })

    const logout = () => {
        localStorage.removeItem("token")
        navigate({to:"/login"})
    }

    return {

        user,
        signUpMutation,
        loginMutation,
        logout
    }
  
}

export {isLoggedIn}
export default useAuth