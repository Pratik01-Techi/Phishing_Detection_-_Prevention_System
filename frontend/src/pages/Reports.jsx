import ReportForm from '../components/ReportForm'

export default function Reports() {
  return (
    <div className="max-w-lg mx-auto px-4 py-8">
      <h1 className="text-2xl font-bold text-textPrimary mb-2">Report a Site</h1>
      <p className="text-textSecondary text-sm mb-6">
        Help protect others by reporting phishing, spam, or malware sites.
      </p>
      <div className="bg-surface rounded-xl border border-gray-800 p-6">
        <ReportForm />
      </div>
    </div>
  )
}
