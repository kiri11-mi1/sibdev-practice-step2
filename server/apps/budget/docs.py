from drf_yasg import openapi


swagger_global_info = {
    'operation_id': 'budget_transaction_global_info',
    'methods': ['GET'],
    'responses': {
        200: openapi.Response(
            description="Вернёт словарь расходов и доходов за выбранный период",
            examples={
                "application/json": {
                    "income": 0.0,
                    "expense": 0.0
                }
            }
        ),
    },
    'tags': ['budget']
}
