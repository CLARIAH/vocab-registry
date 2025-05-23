import {FormEventHandler} from 'react';
import {Controller, FieldErrors, useForm, UseFormRegister, Control} from 'react-hook-form';
import * as Dialog from '@radix-ui/react-dialog';
import MDEditor from '@uiw/react-md-editor';
import useFormSubmissionState, {FormSubmissionState} from '../hooks/useFormSubmission';
import useAuth from '../hooks/useAuth';
import Modal from '../misc/Modal.js';

interface NewVocabInputs {
    title: string;
    homepage: string;
    description: string;
}

export default function RegisterNewVocab() {
    return (
        <Modal triggerElement={<button className="hcButton registerNew">Register new vocabulary</button>}>
            <RegisterNewVocabModalContent/>
        </Modal>
    );
}

function RegisterNewVocabModalContent() {
    const [authEnabled, userInfo] = useAuth();
    const [state, onSubmit, StatusModal] = useFormSubmissionState(onNewVocabInputsSubmit);
    const {register, formState: {errors}, handleSubmit, control} = useForm<NewVocabInputs>();

    async function onNewVocabInputsSubmit(data: NewVocabInputs) {
        const formData = new FormData();
        formData.append('title', data.title);
        formData.append('homepage', data.homepage);
        formData.append('description', data.description);

        return fetch('/vocabulary/new', {
            method: 'POST',
            body: formData,
        });
    }

    if (authEnabled && !userInfo)
        return <LoginMessage/>

    return (
        <StatusModal success="Your vocabulary has been submitted!">
            <RegisterNewVocabForm register={register} errors={errors} control={control}
                                  isDisabled={state === FormSubmissionState.WAITING}
                                  onSubmit={handleSubmit(onSubmit)}/>
        </StatusModal>
    );
}

function LoginMessage() {
    const redirectUri = `/login?redirect-uri=${encodeURIComponent(window.location.href)}`;

    return (
        <>
            <Dialog.Title className="DialogTitle">Login required</Dialog.Title>

            <Dialog.Description className="DialogDescription">
                You need to login first to register a new vocabulary.
            </Dialog.Description>

            <div className="center">
                <a className="hcButton" href={redirectUri}>
                    Log in
                </a>
            </div>
        </>
    );
}

function RegisterNewVocabForm({isDisabled, register, errors, control, onSubmit}: {
    isDisabled: boolean,
    register: UseFormRegister<NewVocabInputs>,
    errors: FieldErrors<NewVocabInputs>,
    control: Control<NewVocabInputs>,
    onSubmit: FormEventHandler
}) {
    return (
        <>
            <Dialog.Title className="DialogTitle">Register a new vocabulary</Dialog.Title>

            <Dialog.Description className="DialogDescription">
                Fill out the details of the vocabulary. Click submit when you're done.
            </Dialog.Description>

            <form onSubmit={onSubmit}>
                <fieldset disabled={isDisabled}>
                    <label className={errors.title ? 'error' : ''}>
                        Title
                        <input {...register('title', {required: true})}
                               type="text" placeholder="The title of the vocabulary"/>
                    </label>

                    <label className={errors.homepage ? 'error' : ''}>
                        Homepage
                        <input {...register('homepage', {required: true})}
                               type="text" placeholder="The homepage of the vocabulary"/>
                    </label>

                    <label className={errors.description ? 'error' : ''}>
                        Description
                        <Controller name="description" control={control} rules={{required: true}}
                                    render={({field: {value, onChange, onBlur}}) => (
                                        <MDEditor className="mdEditor" value={value}
                                                  onChange={onChange} onBlur={onBlur}/>
                                    )}/>
                    </label>

                    <div className="center">
                        <button type="submit" className="hcButton">
                            Submit
                        </button>
                    </div>
                </fieldset>
            </form>
        </>
    );
}
