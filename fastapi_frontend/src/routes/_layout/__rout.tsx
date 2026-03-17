import { createRootRoute, Outlet,HeadContent} from "@tanstack/react-router"
import { TanStackRouterDevtools } from "@tanstack/react-router-devtools"
// import { ErrorComponent } from "@/components/error-component"




export const Route = createRootRoute({
    component: () => {
        <>
            <HeadContent />
            <Outlet />
            <TanStackRouterDevtools position="bottom-right" initialIsOpen={false} />
        </>
    
    },
    // notFoundComponent: () => <div>Not Found</div>,
    // errorComponent: ({ error }: { error: Error }) => <ErrorComponent error={error} />,
})