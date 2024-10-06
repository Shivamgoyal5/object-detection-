module ObjectDetection::ObjectVerifier {

    use aptos_framework::signer;
    use aptos_framework::event;
    use aptos_framework::time;
    use std::address;

    /// Resource type to store detection verification
    struct DetectionResource has key {
        owner: address,
        detection_id: u64,
    }

    /// Event to emit after a successful detection
    struct DetectionEvent has copy, drop, store {
        owner: address,
        detection_id: u64,
        timestamp: u64,
    }

    /// This is used to record the verification event
    public fun emit_detection_event(owner: &signer, detection_id: u64, timestamp: u64) {
        let event = DetectionEvent {
            owner: signer::address_of(owner),
            detection_id,
            timestamp,
        };
        event::emit<DetectionEvent>(&event);
    }

    /// Function to verify detection
    public fun verify_detection(owner: &signer, detection_id: u64) {
        let detection_resource = DetectionResource {
            owner: signer::address_of(owner),
            detection_id,
        };

        // Save detection to the account
        move_to(owner, detection_resource);

        // Emit the detection event with timestamp
        emit_detection_event(owner, detection_id, time::now_seconds());
    }

    /// Function to get detection resource (for example, to see if a detection was verified)
    public fun get_detection(owner: address): DetectionResource acquires DetectionResource {
        borrow_global<DetectionResource>(owner)
    }
}
