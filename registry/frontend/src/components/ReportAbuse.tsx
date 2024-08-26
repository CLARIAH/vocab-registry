import {FormEventHandler} from 'react';
import {FieldErrors, useForm, UseFormRegister} from 'react-hook-form';
import * as Dialog from '@radix-ui/react-dialog';
import useFormSubmissionState, {FormSubmissionState} from '../hooks/useFormSubmission';
import {UserInfo} from '../hooks/useAuth';
import Modal from '../misc/Modal';

interface ReportAbuseInputs {
    name: string;
    email: string;
    description: string;
}

export default function ReportAbuse({id, userInfo}: { id: string, userInfo: UserInfo | null }) {
    return (
        <Modal triggerElement={<button className="hcButton">Report abuse</button>}>
            <ReportAbuseModalContent id={id} userInfo={userInfo}/>
        </Modal>
    );
}

function ReportAbuseModalContent({id, userInfo}: { id: string, userInfo: UserInfo | null }) {
    const [state, onSubmit, StatusModal] = useFormSubmissionState(onReportAbuseSubmit);
    const {
        register,
        formState: {errors},
        handleSubmit
    } = useForm<ReportAbuseInputs>();

    async function onReportAbuseSubmit(data: ReportAbuseInputs) {
        const formData = new FormData();
        formData.append('name', data.name);
        formData.append('email', data.email);
        formData.append('description', data.description);

        return fetch(`/review/${id}/report`, {
            method: 'POST',
            body: formData,
        });
    }

    return (
        <StatusModal success="Your report has been submitted!">
            <ReportAbuseForm userInfo={userInfo} register={register} errors={errors}
                             isDisabled={state === FormSubmissionState.WAITING}
                             onSubmit={handleSubmit(onSubmit)}/>
        </StatusModal>
    );
}

function ReportAbuseForm({isDisabled, userInfo, register, errors, onSubmit}: {
    isDisabled: boolean,
    userInfo: UserInfo | null,
    register: UseFormRegister<ReportAbuseInputs>,
    errors: FieldErrors<ReportAbuseInputs>,
    onSubmit: FormEventHandler
}) {
    return (
        <>
            <Dialog.Title className="DialogTitle">
                Report abuse or inappropriate content
            </Dialog.Title>

            <Dialog.Description className="DialogDescription">
                In case of abuse or inappropriate content is found, please inform site owners via this form
            </Dialog.Description>

            <form onSubmit={onSubmit}>
                <fieldset disabled={isDisabled}>
                    <label className={errors.name ? 'error' : ''}>
                        Name
                        <input {...register('name', {required: true})}
                               type="text" placeholder={userInfo?.nickname}/>
                    </label>

                    <label className={errors.email ? 'error' : ''}>
                        E-mail
                        <input {...register('email', {required: true})}
                               type="email" placeholder={userInfo?.email}/>
                    </label>

                    <label className={errors.description ? 'error' : ''}>
                        Why is the content inappropriate?
                        <textarea {...register('description', {required: true})}/>
                    </label>

                    <div className="center">
                        <button type="submit" className="hcButton">
                            Submit
                        </button>
                    </div>
                </fieldset>
            </form>
        </>
    )
}
