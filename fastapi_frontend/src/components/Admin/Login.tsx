import { useForm } from 'react-hook-form'   
import useAuth from '../../hook/useAuth'
import { Input } from '../ui/input'
import { FormControl, FormField, FormItem, FormLabel, FormMessage } from '../ui/form'

import { Link as RouterLink } from '@tanstack/react-router'
import { AuthLayout } from '../Common/AuthLayout'
import { z } from 'zod'
import { AccessToken } from '../../types/user'

// eslint-disable-next-line @typescript-eslint/no-unused-vars
const formSchema = z.object({
  username: z.email(),
  password: z.string().min(8),
}) satisfies z.ZodType<AccessToken>

type FormData = z.infer<typeof formSchema>
export function Login() {
  const { loginMutation } = useAuth()

  const form = useForm<FormData>({
 
    mode:"onBlur",

    defaultValues: {
      username: '',
      password: '',
    },
  })

  const onSubmit = async (data: FormData) => {
    try {
      await loginMutation.mutateAsync(data)
    } catch (error) {
      console.error('Login failed:', error)
    }
  }
  
  return (
    <AuthLayout>

        <form
          onSubmit={form.handleSubmit(onSubmit)}
          className="flex flex-col gap-4 w-full max-w-sm"
        >
          <div className="grid gap-4">
            <FormField
              control={form.control}
              name="username"
              render={({ field } : { field: any }) => (
                <FormItem>
                  <FormLabel>Email</FormLabel>
                  <FormControl>
                    <Input
                      data-testid="email-input"
                      placeholder="user@example.com"
                      type="email"
                      {...field}
                    />
                  </FormControl>
                  <FormMessage className="text-xs" />
                </FormItem>
              )}
            />

            <FormField
              control={form.control}
              name="password"
              render={({ field } : { field: any }) => (
                <FormItem>
                  <div className="flex items-center">
                    <FormLabel>Password</FormLabel>
                    <RouterLink
                      to="/recover-password"
                      className="ml-auto text-sm underline-offset-4 hover:underline"
                    >
                      Forgot your password?
                    </RouterLink>
                  </div>
                  <FormControl>
                 
                   
                  </FormControl>
                  <FormMessage className="text-xs" />
                </FormItem>
              )}
            />
          </div>
         </form>
    </AuthLayout>
  ) 



}