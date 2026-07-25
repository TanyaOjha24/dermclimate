class IntentRouter:

    def __init__(self, ingredient_service, product_service, weather_service, routine_service):
        self.ingredient_service = ingredient_service
        self.product_service = product_service
        self.weather_service = weather_service
        self.routine_service = routine_service

    def route(self, parsed_request):
        if parsed_request.intent == "ingredient_analysis":
            return self.ingredient_service.analyze(parsed_request)
        elif parsed_request.intent == "product_analysis":
            return self.product_service.analyze(parsed_request)
        elif parsed_request.intent == "weather_query":
            return self.weather_service.analyze(parsed_request)
        elif parsed_request.intent == "routine_recommendation":
            return self.routine_service.analyze(parsed_request)
        else:
            raise ValueError(f"Unknown intent: {parsed_request.intent}")