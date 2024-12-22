"use client";

import { useState } from "react";
import dropdownData from "../content/dropdown_content.json";
import langData from "../content/languages.json";
import { MultiSelect } from "react-multi-select-component";

export default function MainContent() {
  const [languages, setLanguages] = useState([]);
  const [projectTypes, setProjectTypes] = useState([]);
  const [startYear, setStartYear] = useState("");
  const [endYear, setEndYear] = useState("");
  const [comparisonMetric, setComparisonMetric] = useState("");
  const [resultData, setResultData] = useState(null);

  const languageOptions = [
    ...Object.entries(langData).map(([code, lang]) => ({
      label: `${lang.name} (${lang.localname})`,
      value: code,
    })),
  ];

  const comparisonMetricOptions = dropdownData.comparisonMetrics.map((metric) => ({
    label: metric.label,
    value: metric.value,
  }));

  const projectTypeOptions = dropdownData.projectTypes.map((type) => ({
    label: type.label,
    value: type.value,
  }));

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!languages.length || !projectTypes.length || !startYear || !endYear || !comparisonMetric) {
      alert("Please fill in all the fields!");
      return;
    }

    const selectedLanguages = languages.map((lang) => lang.value);
    const selectedProjectTypes = projectTypes.map((type) => type.value);
    const startDate = `${startYear}0101`;
    const endDate = `${endYear}0101`;
    console.log(selectedLanguages, selectedProjectTypes, startDate, endDate, comparisonMetric);

    try {
      const response = await fetch("http://localhost:8000/percentage_change/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          projects: selectedLanguages,
          project_types: selectedProjectTypes,
          start_date: startDate,
          end_date: endDate,
          comparison_metric: comparisonMetric,
        }),
      });

      if (!response.ok) {
        throw new Error(`Error ${response.status}: ${response.statusText}`);
      }

      const data = await response.json();
      setResultData(data);
    } catch (error) {
      console.error("Error fetching data:", error);
    }
  };

  return (
    <section className="container mx-auto py-12 px-6">
      <form onSubmit={handleSubmit} className="space-y-6">
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-6">
          <div>
            <label className="block text-sm font-bold text-gray-700 mb-2">
              Wiki Languages
            </label>
            <MultiSelect
              options={languageOptions}
              value={languages}
              onChange={setLanguages}
              labelledBy="Select languages"
              className="text-gray-700"
            />
          </div>

          <div>
            <label className="block text-sm font-bold text-gray-700 mb-2">
              Project Types
            </label>
            <MultiSelect
              options={projectTypeOptions}
              value={projectTypes}
              onChange={setProjectTypes}
              labelledBy="Select project types"
              className="text-gray-700"
            />
          </div>

          <div>
          <label className="block text-sm font-bold text-gray-700 mb-2">
            Comparison Metric
          </label>
          <select
            className="border border-gray-300 bg-white rounded-md p-3 w-full text-gray-700"
            value={comparisonMetric}
            onChange={(e) => setComparisonMetric(e.target.value)}
          >
            <option value="">Select a metric</option>
            {comparisonMetricOptions.map((option) => (
              <option key={option.value} value={option.value}>
                {option.label}
              </option>
            ))}
          </select>
        </div>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
          <div>
            <label className="block text-sm font-bold text-gray-700 mb-2">
              Start Year
            </label>
            <input
              type="number"
              className="border border-gray-300 bg-white rounded-md p-3 w-full text-gray-700"
              placeholder="YYYY"
              min="2000"
              max="2024"
              value={startYear}
              onChange={(e) => setStartYear(e.target.value)}
            />
          </div>

          <div>
            <label className="block text-sm font-bold text-gray-700 mb-2">
              End Year
            </label>
            <input
              type="number"
              className="border border-gray-300 bg-white rounded-md p-3 w-full text-gray-700"
              placeholder="YYYY"
              min="2000"
              max="2024"
              value={endYear}
              onChange={(e) => setEndYear(e.target.value)}
            />
          </div>
        </div>

        <button
          type="submit"
          className="bg-blue-500 text-white p-3 rounded-md w-full sm:w-auto"
        >
          Submit
        </button>
      </form>

      {resultData && (
        <div className="mt-8 text-gray-700">
          <h2 className="text-lg font-bold mb-4">Results</h2>
          <table className="table-auto w-full border-collapse border border-gray-300">
            <thead>
              <tr>
                <th className="border border-gray-300 px-4 py-2">Metric</th>
                <th className="border border-gray-300 px-4 py-2">Language</th>
                <th className="border border-gray-300 px-4 py-2">Project Type</th>
                <th className="border border-gray-300 px-4 py-2">Value</th>
              </tr>
            </thead>
            <tbody>
              {resultData.map(({ metric, language, project_type, value }) => (
                <tr key={`${metric}-${language}-${project_type}`}>
                  <td className="border border-gray-300 px-4 py-2">{metric}</td>
                  <td className="border border-gray-300 px-4 py-2">{language}</td>
                  <td className="border border-gray-300 px-4 py-2">{project_type}</td>
                  <td className="border border-gray-300 px-4 py-2">{value}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </section>
  );
}

