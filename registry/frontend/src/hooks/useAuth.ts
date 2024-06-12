import {useEffect, useState} from 'react';

export interface UserInfo {
    sub: string;
    email: string;
    nickname: string;
}

export default function useAuth(): [boolean, UserInfo | null] {
    const [authEnabled, setAuthEnabled] = useState(true);
    const [userInfo, setUserInfo] = useState<UserInfo | null>(null);

    useEffect(() => {
        const fetchFromLogin = async () => {
            const response = await fetch('/user-info');
            if (response.ok) {
                const rsp = await response.json();
                setUserInfo(rsp);
                setAuthEnabled(true);
            }
            else {
                setUserInfo(null);
                setAuthEnabled(response.status !== 404);
            }
        };

        fetchFromLogin();
    }, []);

    return [authEnabled, userInfo];
}
