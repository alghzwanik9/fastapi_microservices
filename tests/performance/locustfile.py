from locust import HttpUser, task, between
import random
import string


class UserBehavior(HttpUser):
    wait_time = between(1, 3)
    
    def on_start(self):
        """Called when a simulated user starts"""
        # Register a new user
        self.username = ''.join(random.choices(string.ascii_lowercase, k=10))
        self.email = f"{self.username}@test.com"
        self.password = "testpassword123"
        
        register_response = self.client.post(
            "/api/v1/users/register",
            json={
                "email": self.email,
                "username": self.username,
                "full_name": "Test User",
                "password": self.password
            }
        )
        
        if register_response.status_code == 201:
            # Login to get token
            login_response = self.client.post(
                "/api/v1/users/login",
                json={
                    "username": self.username,
                    "password": self.password
                }
            )
            if login_response.status_code == 200:
                self.token = login_response.json()["access_token"]
                self.headers = {"Authorization": f"Bearer {self.token}"}
    
    @task(3)
    def get_current_user(self):
        """Get current user profile - more frequent"""
        if hasattr(self, 'headers'):
            self.client.get("/api/v1/users/me", headers=self.headers)
    
    @task(2)
    def health_check(self):
        """Check service health"""
        self.client.get("/health")
    
    @task(1)
    def update_profile(self):
        """Update user profile"""
        if hasattr(self, 'headers') and hasattr(self, 'username'):
            self.client.put(
                f"/api/v1/users/1",
                headers=self.headers,
                json={
                    "full_name": f"Updated Name {random.randint(1, 1000)}"
                }
            )


class ProductBehavior(HttpUser):
    """Placeholder for product service load testing"""
    wait_time = between(2, 5)
    
    @task
    def browse_products(self):
        self.client.get("/api/v1/products")


class OrderBehavior(HttpUser):
    """Placeholder for order service load testing"""
    wait_time = between(3, 7)
    
    @task
    def view_orders(self):
        if hasattr(self, 'headers'):
            self.client.get("/api/v1/orders", headers=self.headers)
