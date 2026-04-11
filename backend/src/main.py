"""FastAPI application factory for Vantier backend."""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.core.auth import warm_jwks
from src.core.config import get_settings
from src.core.exceptions import register_exception_handlers


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan: warm up connections and caches on startup."""
    # Pre-fetch Neon Auth JWKS so first request doesn't pay the cost
    await warm_jwks()
    yield
    # Cleanup (if needed in the future)


def create_app() -> FastAPI:
    """Create and configure the FastAPI application instance."""
    settings = get_settings()

    app = FastAPI(
        title="Vantier API",
        version="0.1.0",
        description="Backend for Vantier luxury e-commerce platform",
        docs_url="/docs" if not settings.is_production else None,
        redoc_url="/redoc" if not settings.is_production else None,
        lifespan=lifespan,
    )

    # CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Exception handlers
    register_exception_handlers(app)

    # Routers — uncomment each as the slice is implemented
    from src.features.products.router import router as products_router
    app.include_router(products_router, prefix="/api/v1/products", tags=["Products"])

    # from src.features.inventory.router import router as inventory_router
    # app.include_router(inventory_router, prefix="/api/v1/inventory", tags=["Inventory"])

    # from src.features.orders.router import router as orders_router
    # app.include_router(orders_router, prefix="/api/v1/orders", tags=["Orders"])

    # from src.features.discounts.router import router as discounts_router
    # app.include_router(discounts_router, prefix="/api/v1/discounts", tags=["Discounts"])

    # from src.features.exchanges.router import router as exchanges_router
    # app.include_router(exchanges_router, prefix="/api/v1/exchanges", tags=["Exchanges"])

    # from src.features.purchase_orders.router import router as po_router
    # app.include_router(po_router, prefix="/api/v1/purchase-orders", tags=["Purchase Orders"])

    # from src.features.financials.router import router as financials_router
    # app.include_router(financials_router, prefix="/api/v1/financials", tags=["Financials"])

    # from src.features.users.router import router as users_router
    # app.include_router(users_router, prefix="/api/v1/users", tags=["Users"])

    @app.get("/health", tags=["Health"])
    async def health_check() -> dict:
        """Liveness probe endpoint."""
        return {"status": "ok"}

    return app


app = create_app()
