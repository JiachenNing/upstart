const API_URL = 'http://127.0.0.1:8000';

export interface PollOption {
  option_id: number;
  poll_id: string;
  option_text: string;
  vote_count: number;
}

export interface Poll {
  poll_id: string;
  question: string;
  created_at: string;
  create_by: string | null;
  options: PollOption[];
}

export interface PollCreate {
  question: string;
  options: string[];
  create_by?: string;
}

export const fetchPolls = async (): Promise<Poll[]> => {
  const response = await fetch(`${API_URL}/polls`);
  if (!response.ok) {
    throw new Error('Network response was not ok');
  }
  return response.json();
};

export const fetchPollById = async (pollId: string): Promise<Poll> => {
  const response = await fetch(`${API_URL}/polls/${pollId}`);
  if (!response.ok) {
    throw new Error('Network response was not ok');
  }
  return response.json();
};

export const createPoll = async (poll: PollCreate): Promise<Poll> => {
  const response = await fetch(`${API_URL}/polls`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(poll),
  });
  if (!response.ok) {
    throw new Error('Network response was not ok');
  }
  return response.json();
};
