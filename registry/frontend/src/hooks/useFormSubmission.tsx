import {FC, ReactNode, useState} from 'react';
import ModalSubmissionResult from '../components/ModalSubmissionResult';

export enum FormSubmissionState {
    INITIAL, WAITING, SUCCESS, FAILED
}

export default function useFormSubmissionState<D>(submission: (data: D) => Promise<Response>):
    [FormSubmissionState, (data: D) => Promise<Response>, FC<{ success: string, children: ReactNode }>] {
    const [state, setState] = useState<FormSubmissionState>(FormSubmissionState.INITIAL);

    async function onSubmit(data: D): Promise<Response> {
        setState(FormSubmissionState.WAITING);
        const result = await submission(data);
        setState(result.ok ? FormSubmissionState.SUCCESS : FormSubmissionState.FAILED);
        return result;
    }

    function StatusModal({success, children}: { success: string, children: ReactNode }) {
        return (
            <>
                {[FormSubmissionState.INITIAL, FormSubmissionState.WAITING].includes(state) &&
                    children}
                {[FormSubmissionState.SUCCESS, FormSubmissionState.FAILED].includes(state) &&
                    <ModalSubmissionResult success={state === FormSubmissionState.SUCCESS}
                                           message={state === FormSubmissionState.SUCCESS
                                               ? success
                                               : 'Something went wrong, please try again later!'}/>}
            </>
        );
    }

    return [state, onSubmit, StatusModal];
}
