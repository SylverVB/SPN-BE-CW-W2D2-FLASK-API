# REST API Design Patterns

### REST Resource Naming Conventions
1. Use nouns for resource names
    - `/products`
    - `/orders`
    - `/customers`
2. Use plural nouns for collection names
    - `/products`
    - `/orders`
    - `/customers`
3. Not using singular nouns for resource names
    - `/products/{id}`
    - `/orders/{id}`
    - `/customers/{id}`
4. Use hyphens to separate words
    - `/product-categories`
    - `/product-reviews`
5. Use lowercase letters
    - `/products`
    - `/orders`
    - `/customers`
6. Use query params for filtering, sorting, and pagination
    - `/products?category=electronics`
    - `/products?sort=price`
    - `/products?limit=10&offset=20`