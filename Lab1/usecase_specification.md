
# Use Case Specification

---

# Register Lost Baggage Claim

## Goal

Allow a passenger to register a lost baggage claim so that the airline can initiate baggage tracking and recovery.

---

## Primary Actor

- Passenger

## Supporting Actor

- Baggage Service Agent

---

## Trigger

The passenger realizes that their checked baggage has not arrived after the flight and decides to report it.

---

## Preconditions

1. The passenger has completed their flight.
2. The passenger possesses a valid baggage tag number.
3. The passenger has a valid ticket or booking reference.
4. The Airport Lost Luggage Claim & Tracking Portal is operational.

---

## Postconditions

### Success

- A lost baggage claim is successfully registered.
- A unique Claim ID is generated.
- The baggage recovery process is initiated.
- The claim becomes available to baggage service agents.

### Failure

- No claim is created.
- The passenger is informed about the reason for failure.

---

## Main Success Scenario

1. The passenger opens the Airport Lost Luggage Claim & Tracking Portal.
2. The passenger selects **Register Lost Baggage Claim**.
3. The system prompts the passenger to enter:
   - Baggage Tag Number
   - Flight Number
   - Passenger Details
4. The passenger enters the required information.
5. The system validates the submitted details.
6. The system searches baggage scan records across connected airport terminals.
7. The system creates a new lost baggage claim.
8. The system generates a unique Claim ID.
9. The system displays a confirmation message.
10. The passenger can later use the Claim ID to track baggage status.

---

## Alternate Flow

### 	Invalid Baggage Tag Number

1. The passenger enters an invalid baggage tag number.
2. The system detects that the baggage tag cannot be verified.
3. The system displays an error message indicating that the baggage tag is invalid.
4. The passenger re-enters the correct baggage information.
5. The use case resumes from Step 5 of the Main Success Scenario.

---

## Business Rules

- Every baggage claim must be associated with exactly one baggage tag.
- A Claim ID must be unique.
- Only authenticated baggage service agents may update the claim status.
- Compensation processing can begin only after baggage is declared unrecoverable according to airline policy.
