/**
 * API Client for Interview Practice System
 * Connects to backend microservices
 */

import axios from 'axios';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

const apiClient = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add response interceptor to handle FastAPI validation errors
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    // Extract error message from FastAPI validation format
    if (error.response?.data?.detail) {
      const detail = error.response.data.detail;
      if (Array.isArray(detail)) {
        // FastAPI validation errors are arrays
        error.message = detail.map((e: any) => e.msg || e.message || String(e)).join(', ');
      } else if (typeof detail === 'string') {
        error.message = detail;
      } else if (typeof detail === 'object') {
        error.message = JSON.stringify(detail);
      }
    }
    return Promise.reject(error);
  }
);

// Types
export interface SessionCreate {
  resume: string;
  job_description: string;
  interview_type: 'Behavioral' | 'Technical' | 'Mixed';
}

export interface Session {
  session_id: string;
  status: string;
  question_count: number;
  answer_count: number;
  current_question: string | null;
}

export interface Question {
  session_id: string;
  question: string;
  question_number: number;
  question_type: string;
  followup_needed: boolean;
  audio?: string;
}

export interface AnswerSubmission {
  answer: string;
  collect_mode?: boolean;
}

export interface Evaluation {
  question: string;
  answer: string;
  scores: {
    clarity: number;
    communication: number;
    star_structure: number;
    role_relevance: number;
    technical_depth: number;
    overall: number;
  };
  feedback: {
    strengths: string[];
    improvements: string[];
    sample_answer: string;
  };
}

export interface FinalReport {
  session_id: string;
  average_score: number;
  detailed_scores: {
    clarity: number;
    communication: number;
    star_structure: number;
    role_relevance: number;
    technical_depth: number;
    overall: number;
  };
  key_strengths: string[];
  key_improvements: string[];
  recommended_topics: string[];
  next_focus: string;
  total_questions: number;
  total_answers: number;
  audio_summary?: string;
}

// API Functions
export const api = {
  // Health check
  healthCheck: async () => {
    const response = await apiClient.get('/health');
    return response.data;
  },

  // Session management
  createSession: async (data: SessionCreate): Promise<Session> => {
    const response = await apiClient.post('/api/sessions', data);
    return response.data;
  },

  getSession: async (sessionId: string): Promise<Session> => {
    const response = await apiClient.get(`/api/sessions/${sessionId}`);
    return response.data;
  },

  // Interview flow
  startInterview: async (sessionId: string): Promise<Question> => {
    const response = await apiClient.post(`/api/sessions/${sessionId}/start`);
    return response.data;
  },

  submitAnswer: async (
    sessionId: string,
    answer: string,
    collectMode: boolean = true
  ) => {
    const response = await apiClient.post(
      `/api/sessions/${sessionId}/submit-answer?collect_mode=${collectMode}`,
      { answer: answer }
    );
    return response.data;
  },

  getNextQuestion: async (sessionId: string): Promise<Question> => {
    const response = await apiClient.post(
      `/api/sessions/${sessionId}/next-question`
    );
    return response.data;
  },

  // Evaluation
  evaluateAll: async (sessionId: string): Promise<{
    session_id: string;
    evaluations: Evaluation[];
    total_evaluated: number;
  }> => {
    const response = await apiClient.post(
      `/api/sessions/${sessionId}/evaluate-all`
    );
    return response.data;
  },

  endInterview: async (sessionId: string): Promise<FinalReport> => {
    const response = await apiClient.post(`/api/sessions/${sessionId}/end`);
    return response.data;
  },

  // Voice
  transcribeAudio: async (audioData: string) => {
    const response = await apiClient.post('/api/voice/transcribe', {
      audio_data: audioData,
    });
    return response.data;
  },
};

