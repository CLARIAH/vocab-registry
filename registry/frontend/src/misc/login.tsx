import * as Dialog from '@radix-ui/react-dialog';

export const getLoginUrl = () => `/login?redirect-uri=${window.location.protocol + '//' + window.location.host + window.location.pathname}`;

export const loginAction = () => window.location.href = getLoginUrl();

export function LoginRequiredModalContent() {
    return (
        <>
            <Dialog.Title className="DialogTitle">Login required</Dialog.Title>

            <Dialog.Description className="DialogDescription">
                We use the CLARIAH infrastructure allowing you to login with the account of your organisation (e.g.,
                university or institute).
            </Dialog.Description>

            <div className="center">
                <button className="hcButton" aria-label="Login" onClick={loginAction}>
                    Login
                </button>
            </div>
        </>
    );
}
