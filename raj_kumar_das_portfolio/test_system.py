import app
import json

def test_full_pipeline():
    app.init_db()

    with app.app.test_client() as client:
        print("\n--- 1. TESTING PUBLIC CONTACT FORM API ---")
        contact_payload = {
            'name': 'Test Recruiter',
            'email': 'recruiter@company.com',
            'subject': 'Software Engineering Opportunity',
            'message': 'Hi Raj, we reviewed your portfolio and SentinelAI project. We would love to schedule an interview!'
        }
        res = client.post('/api/contact', data=contact_payload)
        print(f"Contact Submission Response Code: {res.status_code}")
        data = res.get_json()
        print(f"Contact Response Data: {data}")
        assert res.status_code == 200
        assert data['success'] is True

        print("\n--- 2. VERIFYING DATABASE PERSISTENCE ---")
        with app.app.app_context():
            saved_msg = app.Message.query.filter_by(email='recruiter@company.com').first()
            assert saved_msg is not None
            print(f"Found Saved Message in DB! ID: {saved_msg.id}, Name: {saved_msg.name}, Status: {saved_msg.status}")

        print("\n--- 3. TESTING ADMIN AUTHENTICATION ---")
        # Test Invalid Login
        bad_login = client.post('/admin/login', data={'email': 'admin@rajkumardas.dev', 'password': 'WrongPassword!'})
        assert b'Invalid email or password' in bad_login.data
        print("Invalid password rejected successfully.")

        # Test Valid Login
        login_res = client.post('/admin/login', data={'email': 'admin@rajkumardas.dev', 'password': 'Admin@12345'}, follow_redirects=True)
        assert login_res.status_code == 200
        assert b'Portfolio Administration Overview' in login_res.data
        print("Admin authenticated and redirected to Dashboard successfully!")

        print("\n--- 4. TESTING ADMIN INBOX & STATUS UPDATE ---")
        inbox_res = client.get('/admin/messages')
        assert inbox_res.status_code == 200
        assert b'Software Engineering Opportunity' in inbox_res.data
        print("Submitted message is visible in Admin Messages Inbox!")

        # Update Status to Read
        status_res = client.post(f'/admin/api/messages/{saved_msg.id}/status', json={'status': 'Read'})
        assert status_res.status_code == 200
        assert status_res.get_json()['new_status'] == 'Read'
        print("Message status successfully updated to Read via API!")

        print("\n--- 5. TESTING ADMIN MESSAGE DELETION ---")
        del_res = client.post(f'/admin/api/messages/{saved_msg.id}/delete')
        assert del_res.status_code == 200
        assert del_res.get_json()['success'] is True
        
        with app.app.app_context():
            deleted_check = app.db.session.get(app.Message, saved_msg.id)
            assert deleted_check is None
            print("Message successfully deleted from DB!")

    print("\n==========================================")
    print("ALL SYSTEM INTEGRATION TESTS PASSED 100%!")
    print("==========================================")

if __name__ == '__main__':
    test_full_pipeline()
