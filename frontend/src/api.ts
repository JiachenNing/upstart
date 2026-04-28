const API_URL = 'http://127.0.0.1:8000';

export interface Submission {
  id: number;
  name: string;
  email: string;
  phone: string;
  gender: string | null;
  message: string;
}

export interface SubmissionCreate {
  name: string;
  email: string;
  phone: string;
  gender: string;
  message: string;
}

export const fetchSubmissions = async (): Promise<Submission[]> => {
  const response = await fetch(`${API_URL}/submissions/`);
  if (!response.ok) {
    throw new Error('Network response was not ok');
  }
  return response.json();
};

export const createSubmission = async (submission: SubmissionCreate): Promise<Submission> => {
  const response = await fetch(`${API_URL}/submissions/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(submission),
  });
  if (!response.ok) {
    throw new Error('Network response was not ok');
  }
  return response.json();
};
