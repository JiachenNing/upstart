import { FormEvent, useEffect, useState } from 'react';
import { Poll, createPoll, fetchPollById, fetchPolls } from './api';

function App() {
  const [polls, setPolls] = useState<Poll[]>([]);
  const [loading, setLoading] = useState(true);

  const [isCreating, setIsCreating] = useState(false);
  const [question, setQuestion] = useState('');
  const [options, setOptions] = useState<string[]>(['', '']);
  const [createBy, setCreateBy] = useState('');
  const [submitting, setSubmitting] = useState(false);

  const [selectedPoll, setSelectedPoll] = useState<Poll | null>(null);
  const [selectedOptionId, setSelectedOptionId] = useState<number | null>(null);

  const isFormComplete =
    question.trim() !== '' &&
    options.every((optionText) => optionText.trim() !== '');

  const loadPolls = async () => {
    setLoading(true);
    try {
      const data = await fetchPolls();
      setPolls(data);
    } catch (error) {
      console.error('Failed to fetch polls:', error);
    }
    setLoading(false);
  };

  useEffect(() => {
    loadPolls();
  }, []);

  const handleOptionInputChange = (index: number, value: string) => {
    setOptions((prevOptions) => prevOptions.map((optionText, i) => (i === index ? value : optionText)));
  };

  const resetForm = () => {
    setQuestion('');
    setOptions(['', '']);
    setCreateBy('');
  };

  const handleAddMoreOption = () => {
    setOptions((prevOptions) => [...prevOptions, '']);
  };

  const handleCreatePoll = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    if (!isFormComplete) return;
    setSubmitting(true);

    try {
      await createPoll({
        question: question.trim(),
        options: options.map((optionText) => optionText.trim()),
        create_by: createBy.trim() || undefined,
      });
      setIsCreating(false);
      resetForm();
      await loadPolls();
    } catch (error) {
      console.error('Failed to create poll:', error);
    }

    setSubmitting(false);
  };

  const handleOpenPoll = async (pollId: string) => {
    try {
      const poll = await fetchPollById(pollId);
      setSelectedPoll(poll);
      setSelectedOptionId(null);
    } catch (error) {
      console.error('Failed to fetch poll details:', error);
    }
  };

  return (
    <div className="app-container">
      <header className="page-header">
        <h1>Polls</h1>
        {!selectedPoll && (
          <button
            type="button"
            className="primary-btn"
            onClick={() => setIsCreating((prev) => !prev)}
          >
            {isCreating ? 'Cancel' : 'Add'}
          </button>
        )}
      </header>

      {isCreating && !selectedPoll && (
        <section className="panel">
          <h2>Create New Poll</h2>
          <form onSubmit={handleCreatePoll} className="poll-form">
            <label className="field">
              <span>Question</span>
              <input
                type="text"
                value={question}
                onChange={(e) => setQuestion(e.target.value)}
                placeholder="Enter poll question"
                required
              />
            </label>

            {options.map((optionText, index) => (
              <label className="field" key={index}>
                <span>Option {index + 1}</span>
                <input
                  type="text"
                  value={optionText}
                  onChange={(e) => handleOptionInputChange(index, e.target.value)}
                  placeholder={`Enter option ${index + 1}`}
                  required
                />
              </label>
            ))}
            <button
              type="button"
              className="secondary-btn"
              onClick={handleAddMoreOption}
            >
              Add More
            </button>

            <label className="field">
              <span>Created By (optional)</span>
              <input
                type="text"
                value={createBy}
                onChange={(e) => setCreateBy(e.target.value)}
                placeholder="Your name"
              />
            </label>

            <button type="submit" className="primary-btn" disabled={submitting || !isFormComplete}>
              {submitting ? 'Creating...' : 'Submit'}
            </button>
          </form>
        </section>
      )}

      <main className="main-content">
        {!selectedPoll ? (
          <section className="panel">
            <h2>All Polls</h2>
            {loading ? (
              <p className="empty-state">Loading polls...</p>
            ) : polls.length === 0 ? (
              <p className="empty-state">No polls yet. Click Add to create one.</p>
            ) : (
              <div className="poll-grid">
                {polls.map((poll) => (
                  <button
                    key={poll.poll_id}
                    type="button"
                    className="poll-card"
                    onClick={() => void handleOpenPoll(poll.poll_id)}
                  >
                    <h3>{poll.question}</h3>
                    <p>{poll.options.length} options</p>
                  </button>
                ))}
              </div>
            )}
          </section>
        ) : (
          <section className="panel">
            <div className="detail-header">
              <button type="button" className="secondary-btn" onClick={() => setSelectedPoll(null)}>
                Back to Polls
              </button>
              <h2>Poll Detail</h2>
            </div>
            <h3 className="poll-question">{selectedPoll.question}</h3>
            <div className="option-list">
              {selectedPoll.options.map((option) => (
                <label key={option.option_id} className="option-item">
                  <input
                    type="radio"
                    name="selected-option"
                    value={option.option_id}
                    checked={selectedOptionId === option.option_id}
                    onChange={() => setSelectedOptionId(option.option_id)}
                  />
                  <span>{option.option_text}</span>
                </label>
              ))}
            </div>
            <button
              type="button"
              className="primary-btn vote-btn"
              disabled={selectedOptionId === null}
              onClick={() => window.alert('Vote endpoint is not implemented yet.')}
            >
              Vote
            </button>
          </section>
        )}
      </main>
    </div>
  );
}

export default App;
