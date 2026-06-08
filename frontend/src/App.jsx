import { useMemo, useState } from 'react';

const API_BASE_URL = 'http://localhost:8000';

function App() {
  const [file, setFile] = useState(null);
  const [report, setReport] = useState('');
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [copyStatus, setCopyStatus] = useState('');

  const canSubmit = useMemo(() => file && !isLoading, [file, isLoading]);

  const handleFileChange = (event) => {
    setError('');
    const selected = event.target.files?.[0] ?? null;
    setFile(selected);
  };

  const handleGenerate = async (event) => {
    event.preventDefault();
    if (!file) {
      setError('画像を選択してください。');
      return;
    }

    try {
      setIsLoading(true);
      setCopyStatus('');
      setError('');

      const formData = new FormData();
      formData.append('image', file);

      const response = await fetch(`${API_BASE_URL}/api/reports/generate`, {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        const payload = await response.json().catch(() => ({}));
        const message = payload.detail ?? '日報の生成に失敗しました。';
        throw new Error(message);
      }

      const payload = await response.json();
      setReport(payload.report ?? '');
    } catch (requestError) {
      setError(requestError.message);
    } finally {
      setIsLoading(false);
    }
  };

  const handleCopy = async () => {
    if (!report) {
      return;
    }

    try {
      await navigator.clipboard.writeText(report);
      setCopyStatus('コピーしました');
    } catch {
      setCopyStatus('コピーに失敗しました');
    }
  };

  return (
    <main className="page">
      <section className="card">
        <h1>Daily Report Generator</h1>
        <p className="lead">スクリーンショットから日報を自動生成します。</p>

        <form onSubmit={handleGenerate} className="form">
          <label htmlFor="image" className="field-label">
            画像アップロード（JPEG / PNG, 最大5MB）
          </label>
          <input
            id="image"
            className="file-input"
            type="file"
            accept="image/png,image/jpeg"
            onChange={handleFileChange}
          />

          <button type="submit" disabled={!canSubmit} className="primary-button">
            {isLoading ? '生成中...' : '日報を生成'}
          </button>
        </form>

        {error ? <p className="message error">{error}</p> : null}

        <section className="result">
          <div className="result-header">
            <h2>生成結果</h2>
            <button type="button" onClick={handleCopy} className="ghost-button" disabled={!report}>
              コピー
            </button>
          </div>

          <textarea
            className="report-textarea"
            value={report}
            onChange={(event) => setReport(event.target.value)}
            placeholder="ここに生成された日報が表示されます。"
          />
          {copyStatus ? <p className="message">{copyStatus}</p> : null}
        </section>
      </section>
    </main>
  );
}

export default App;
