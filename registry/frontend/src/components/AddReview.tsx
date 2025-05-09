import {FormEventHandler} from 'react';
import {useRevalidator} from 'react-router-dom';
import {FieldErrors, useForm, UseFormRegister, UseFormSetValue} from 'react-hook-form';
import {Rating} from 'react-simple-star-rating';
import * as Dialog from '@radix-ui/react-dialog';
import useFormSubmissionState, {FormSubmissionState} from '../hooks/useFormSubmission';
import {UserInfo} from '../hooks/useAuth';
import Modal from '../misc/Modal';
import {Vocab} from '../misc/interfaces';

interface AddReviewInputs {
    rating: number;
    body: string;
}

export default function AddReview({data, authEnabled, userInfo}: {
    data: Vocab,
    authEnabled: boolean,
    userInfo: UserInfo | null
}) {
    const revalidator = useRevalidator();

    if (authEnabled && !userInfo) {
        const redirectUri = `/login?redirect-uri=${encodeURIComponent(window.location.href)}`;
        return (
            <a className="hcButton" href={redirectUri}>
                Login to add a review
            </a>
        );
    }

    return (
        <Modal triggerElement={<button className="hcButton">Add review</button>}
               onClose={() => revalidator.revalidate()}>
            <AddReviewModalContent vocab={data}/>
        </Modal>
    );
}

function AddReviewModalContent({vocab}: { vocab: Vocab }) {
    const [state, onSubmit, StatusModal] = useFormSubmissionState(onAddReviewSubmit);
    const {
        register,
        formState: {errors},
        setValue,
        handleSubmit
    } = useForm<AddReviewInputs>();

    async function onAddReviewSubmit(data: AddReviewInputs) {
        const formData = new FormData();
        formData.append('rating', data.rating.toString());
        formData.append('body', data.body);

        return fetch(`/review/${vocab.identifier}`, {
            method: 'POST',
            body: formData,
        });
    }

    return (
        <StatusModal success="Your review has been submitted!">
            <AddReviewForm vocab={vocab} register={register} errors={errors} setValue={setValue}
                           isDisabled={state === FormSubmissionState.WAITING}
                           onSubmit={handleSubmit(onSubmit)}/>
        </StatusModal>
    );
}

function AddReviewForm({isDisabled, vocab, register, errors, setValue, onSubmit}: {
    isDisabled: boolean,
    vocab: Vocab,
    register: UseFormRegister<AddReviewInputs>,
    errors: FieldErrors<AddReviewInputs>,
    setValue: UseFormSetValue<AddReviewInputs>,
    onSubmit: FormEventHandler
}) {
    register('rating', {required: true, min: 0.5, max: 5});

    return (
        <>
            <Dialog.Title className="DialogTitle">
                Add a review
            </Dialog.Title>

            <Dialog.Description className="DialogDescription">
                Add a review for "{vocab.title}"
            </Dialog.Description>

            <form onSubmit={onSubmit}>
                <fieldset disabled={isDisabled}>
                    <label className={errors.rating ? 'error' : ''}>
                        <Rating initialValue={0} readonly={false} showTooltip={false} size={30}
                                onClick={value => setValue('rating', value)}/>
                    </label>

                    <label className={errors.body ? 'error' : ''}>
                        <textarea {...register('body', {required: true})}/>
                    </label>

                    <div className="center">
                        <button type="submit" className="hcButton">
                            Post review
                        </button>
                    </div>
                </fieldset>
            </form>
        </>
    );
}
