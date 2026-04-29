import { useEffect, useState } from 'react';
import { Submission, fetchSubmissions, createSubmission, deleteSubmission } from './api';

function App() {
  const [submissions, setSubmissions] = useState<Submission[]>([]);
  const [loading, setLoading] = useState(true);
  
  const [name, setName] = useState('');
  const [userName, setUserName] = useState('');
  const [email, setEmail] = useState('');
  const [phone, setPhone] = useState('');
  const [gender, setGender] = useState('');
  const [message, setMessage] = useState('');
  const [submitting, setSubmitting] = useState(false);
  const [deletingSubmissionId, setDeletingSubmissionId] = useState<number | null>(null);
  const isFormComplete = [name, email, phone, gender, message].every(field => field.trim() !== '');

  const loadSubmissions = async () => {
    setLoading(true);
    try {
      const data = await fetchSubmissions();
      setSubmissions(data);
    } catch (error) {
      console.error('Failed to fetch submissions:', error);
    }
    setLoading(false);
  };

  useEffect(() => {
    loadSubmissions();
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!isFormComplete) return;
    setSubmitting(true);
    try {
      await createSubmission({ name, userName: userName.trim() || undefined, email, phone, gender, message });
      setName('');
      setUserName('');
      setEmail('');
      setPhone('');
      setGender('');
      setMessage('');
      await loadSubmissions();
      // Optionally show a success toast here
    } catch (error) {
      console.error('Failed to create submission:', error);
    }
    setSubmitting(false);
  };

  const handleDeleteSubmission = async (submissionId: number) => {
    const shouldDelete = window.confirm('Delete this submission? This action cannot be undone.');
    if (!shouldDelete) return;

    setDeletingSubmissionId(submissionId);
    try {
      await deleteSubmission(submissionId);
      setSubmissions((prev) => prev.filter((submission) => submission.id !== submissionId));
    } catch (error) {
      console.error('Failed to delete submission:', error);
    }
    setDeletingSubmissionId(null);
  };

  return (
    <div className="app-container">
      <main className="main-content">
        <section className="form-section">
          <div className="glass-card">
            <h2>Submit Form</h2>
            <form onSubmit={handleSubmit}>
              <div className="input-group">
                <input 
                  type="text" 
                  id="name"
                  placeholder=" "
                  value={name}
                  onChange={e => setName(e.target.value)}
                  required 
                />
                <label htmlFor="name">Full Name</label>
              </div>

              <div className="input-group">
                <input 
                  type="text" 
                  id="userName"
                  placeholder=" "
                  value={userName}
                  onChange={e => setUserName(e.target.value)}
                />
                <label htmlFor="userName">UserName</label>
              </div>

              <div className="input-group">
                <input 
                  type="email" 
                  id="email"
                  placeholder=" "
                  value={email}
                  onChange={e => setEmail(e.target.value)}
                  required 
                />
                <label htmlFor="email">Email Address</label>
              </div>

              <div className="input-group">
                <input
                  type="tel"
                  id="phone"
                  placeholder=" "
                  value={phone}
                  onChange={e => setPhone(e.target.value)}
                  required
                />
                <label htmlFor="phone">Phone Number</label>
              </div>

              <div className="input-group">
                <select
                  id="gender"
                  value={gender}
                  onChange={e => setGender(e.target.value)}
                  required
                >
                  <option value="" disabled>Select Gender</option>
                  <option value="Male">Male</option>
                  <option value="Female">Female</option>
                  <option value="Non-binary">Non-binary</option>
                  <option value="Prefer not to say">Prefer not to say</option>
                </select>
              </div>

              <div className="input-group">
                <textarea 
                  id="message"
                  placeholder=" "
                  rows={4}
                  value={message}
                  onChange={e => setMessage(e.target.value)}
                  required 
                />
                <label htmlFor="message">Your Message</label>
              </div>

              <button type="submit" disabled={submitting || !isFormComplete} className="submit-btn">
                {submitting ? 'Sending...' : 'Send Message'}
                <span className="btn-glow"></span>
              </button>
            </form>
          </div>
        </section>

        <section className="data-section">
          <h2>Recent Submissions</h2>
          <div className="submissions-grid">
            {loading ? (
              <div className="loader"></div>
            ) : submissions.length === 0 ? (
              <p className="empty-state">No submissions yet. Be the first!</p>
            ) : (
              submissions.map(sub => (
                <div key={sub.id} className="submission-card">
                  <button
                    type="button"
                    className="delete-submission-btn"
                    aria-label={`Delete submission ${sub.id}`}
                    title="Delete submission"
                    disabled={deletingSubmissionId === sub.id}
                    onClick={() => void handleDeleteSubmission(sub.id)}
                  >
                    {deletingSubmissionId === sub.id ? '...' : '\u00d7'}
                  </button>
                  <div className="submission-header">
                    <span className="avatar">{sub.name.charAt(0).toUpperCase()}</span>
                    <div>
                      <h3>{sub.name}</h3>
                      <div>{sub.userName ?? 'Not provided'}</div>
                      <span className="email">{sub.email}</span>
                      <div>{sub.phone}</div>
                      <div>{sub.gender ?? 'Not provided'}</div>
                    </div>
                  </div>
                  <p className="message">{sub.message}</p>
                </div>
              ))
            )}
          </div>
        </section>
      </main>
    </div>
  );
}

export default App;
