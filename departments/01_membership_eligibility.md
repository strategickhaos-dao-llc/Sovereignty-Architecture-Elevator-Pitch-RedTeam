# Membership Eligibility Department

## Purpose
Handles all questions related to Navy Federal Credit Union membership eligibility criteria and verification.

## Key Questions Handled

### 1. Primary Eligibility Question
**Q: Do you qualify for Navy Federal membership?**

**Process:**
- Verify if applicant meets ANY of the following criteria:
  - Currently enlisted in U.S. military (Active Duty, Guard, or Reserves)
  - Military veteran
  - Department of Defense (DOD) civilian employee
  - DOD contractor
  - Immediate family member in Navy Federal
  - Household member in Navy Federal

**Decision Tree:**
```
IF any_criteria_met = TRUE
  THEN → Proceed to Business Account Services Department
ELSE
  THEN → Route to Alternative Banking Solutions Department
END
```

## Documentation Required
- Military service records (DD-214 for veterans)
- DOD employment verification
- Contractor documentation
- Family member Navy Federal account information

## Response Templates

### Eligible Response
```
✅ ELIGIBLE FOR NAVY FEDERAL MEMBERSHIP

Based on your [military service/DOD employment/family connection], 
you qualify for Navy Federal membership.

Next Steps:
→ Proceed to Business Account Services Department
→ Review required business documentation
```

### Not Eligible Response
```
❌ NOT ELIGIBLE FOR NAVY FEDERAL MEMBERSHIP

Navy Federal is a DOD-restricted credit union with strict membership rules.
You do not currently meet eligibility criteria.

Next Steps:
→ Proceed to Alternative Banking Solutions Department
→ Review alternative banking options for your business entities
```

## Department Contacts
- **Lead:** Eligibility Verification Officer
- **Support:** Membership Documentation Team
- **Escalation:** Navy Federal Liaison Officer

## Related Departments
- [Business Account Services](02_business_account_services.md)
- [Alternative Banking Solutions](04_alternative_banking_solutions.md)
- [Eligibility Verification](05_eligibility_verification.md)
