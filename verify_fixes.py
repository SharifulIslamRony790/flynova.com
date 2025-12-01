from django.contrib.auth import get_user_model
from reportlab.pdfgen import canvas
import io

User = get_user_model()

def test_user_deletion():
    print("\n--- Testing User Deletion & Re-signup ---")
    email = "test_delete@example.com"
    username = "test_delete_user"
    password = "password123"

    # 1. Create user
    try:
        user = User.objects.create_user(username=username, email=email, password=password)
        print(f"[OK] User created: {user.email}")
    except Exception as e:
        print(f"[FAIL] Failed to create user: {e}")
        # Try to get existing user to clean up
        try:
            user = User.objects.get(email=email)
            print(f"[INFO] User already existed, retrieved: {user.email}")
        except:
            return

    # 2. Delete user
    try:
        user.delete()
        print(f"[OK] User deleted: {email}")
    except Exception as e:
        print(f"[FAIL] Failed to delete user: {e}")
        return

    # 3. Try to create user again with same email
    try:
        user = User.objects.create_user(username=username, email=email, password=password)
        print(f"[OK] User RE-CREATED successfully with same email: {user.email}")
        print("[SUCCESS] CONCLUSION: Deleting a user frees up the email address correctly.")
        # Cleanup
        user.delete()
    except Exception as e:
        print(f"[FAIL] Failed to re-create user: {e}")

def test_pdf_generation():
    print("\n--- Testing PDF Generation ---")
    try:
        buffer = io.BytesIO()
        p = canvas.Canvas(buffer)
        p.drawString(100, 100, "Hello world")
        p.showPage()
        p.save()
        pdf_data = buffer.getvalue()
        buffer.close()
        print(f"[OK] PDF generated successfully. Size: {len(pdf_data)} bytes")
        print("[SUCCESS] CONCLUSION: reportlab library is installed and working.")
    except Exception as e:
        print(f"[FAIL] PDF generation failed: {e}")
        print("[FAIL] CONCLUSION: reportlab library is NOT working properly.")

if __name__ == "__main__":
    test_user_deletion()
    test_pdf_generation()
