from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .utils import send_prompt_to_gemini

class GeminiPromptView(APIView):
    def post(self, request):
        prompt = request.data.get("prompt")
        if not prompt:
            return Response({"error": "Prompt is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            gemini_response = send_prompt_to_gemini(prompt)
            return Response({"response": gemini_response}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)