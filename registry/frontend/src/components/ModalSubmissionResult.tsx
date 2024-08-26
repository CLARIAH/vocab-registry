import * as Dialog from '@radix-ui/react-dialog';
import {FontAwesomeIcon} from '@fortawesome/react-fontawesome';
import {faCheck, faTriangleExclamation} from '@fortawesome/free-solid-svg-icons';

export default function ModalSubmissionResult({success, message}: { success: boolean, message: string }) {
    return (
        <div className="center">
            <FontAwesomeIcon icon={success ? faCheck : faTriangleExclamation} size="4x"
                             className={success ? 'success' : 'failure'}/>

            <Dialog.Description className="DialogDescription">
                {message}
            </Dialog.Description>
        </div>
    );
}
