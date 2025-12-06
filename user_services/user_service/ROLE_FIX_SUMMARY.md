# Role Passing Fix - Summary

## Problem
The `role` field from `auth_service` was not being saved to the `Profile` model in `user_service` when a user was created.

## Root Cause
The `handle_user_created_event` function in `infrastructure/message_broker.py` was:
1. ❌ Not extracting the `role` from the event data
2. ❌ Using incorrect field (`username` instead of `first_name`)
3. ❌ Not saving the `role` field to the Profile model

## Solution Applied

### Fixed `handle_user_created_event` function:
- ✅ Now extracts `role` from event data: `role = data.get("role", "client")`
- ✅ Fixed field extraction to use `first_name` instead of `username`
- ✅ Saves `role` to Profile model using `update_or_create`
- ✅ Added error handling for robustness
- ✅ Uses `update_or_create` to handle both new and existing profiles

### Changes Made:
```python
# Before:
Profile.objects.create(
    auth_user_id=data["id"],
    first_name=data.get("username", ""),  # Wrong field
    last_name=""  # Role not saved
)

# After:
profile, created = Profile.objects.update_or_create(
    auth_user_id=auth_user_id,
    defaults={
        "first_name": first_name,
        "last_name": last_name,
        "role": role,  # ✅ Role is now saved
    }
)
```

## Event Flow

1. **auth_service** creates user and publishes event:
   ```json
   {
     "event": "USER_CREATED",
     "id": 1,
     "email": "user@example.com",
     "first_name": "John",
     "last_name": "Doe",
     "role": "architect"  // ✅ Role is included
   }
   ```

2. **RabbitMQ** delivers event to user_service

3. **user_service** consumer receives event and now saves:
   - ✅ auth_user_id
   - ✅ first_name
   - ✅ last_name
   - ✅ **role** (NEWLY FIXED)

## Testing

To verify the fix works:

1. Create a new user through auth_service API with a role
2. Check RabbitMQ logs for the event being sent
3. Check user_service logs for the profile being created/updated
4. Verify in database that Profile.role field has the correct value

## Files Modified

- `user_services/user_service/infrastructure/message_broker.py`
  - Fixed `handle_user_created_event` function to extract and save role

## Next Steps

1. Restart the user_service to apply changes
2. Test by creating a new user with different roles
3. Verify roles are correctly saved in the Profile model

