"use client";

import { useState } from "react";
import dropdownData from "../content/dropdown_content.json";
import langData from "../content/languages.json";
import { MultiSelect } from "react-multi-select-component";

export default function MainContent() {
  const [languages, setLanguages] = useState([{ label: "All", value: "all" }]);
  const [projectType, setProjectType] = useState("");
  const [startYear, setStartYear] = useState("");
  const [endYear, setEndYear] = useState("");
  const [resultData, setResultData] = useState(null);

  // Options for the multiselect dropdown
  const languageOptions = [
    { label: "All", value: "all" },
    ...Object.entries(langData).map(([code, lang]) => ({
      label: `${lang.name} (${lang.localname})`,
      value: code,
    })),
  ];

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!languages.length || !projectType || !startYear || !endYear) {
      alert("Please fill in all the fields!");
      return;
    }

    // Handle "All" option
    const selectedLanguages =
      languages.some((lang) => lang.value === "all")
        ? languageOptions.filter((lang) => lang.value !== "all").map((lang) => lang.value)
        : languages.map((lang) => lang.value);

    const startDate = `${startYear}0101`;
    const endDate = `${endYear}0101`;

    try {
      const response = await fetch("http://localhost:8000/percentage_change/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          projects: selectedLanguages.map((lang) => `${lang}.${projectType}.org`),
          start_date: startDate,
          end_date: endDate,
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
          {/* Multiselect for Languages */}
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

          {/* Dropdown for Project Type */}
          <div>
            <label className="block text-sm font-bold text-gray-700 mb-2">
              Project Type
            </label>
            <select
              className="border border-gray-300 bg-white rounded-md p-3 w-full text-gray-700 focus:ring-2 focus:ring-blue-500"
              value={projectType}
              onChange={(e) => setProjectType(e.target.value)}
            >
              <option value="" disabled>
                Select a project type
              </option>
              {dropdownData.projectTypes.map((type) => (
                <option key={type.value} value={type.value}>
                  {type.label}
                </option>
              ))}
            </select>
          </div>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
          {/* Date Picker for Start Year */}
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

          {/* Date Picker for End Year */}
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

      {/* Result Table */}
      {resultData && (
        <div className="mt-8 text-gray-700">
          <h2 className="text-lg font-bold mb-4">Results</h2>
          <table className="table-auto w-full border-collapse border border-gray-300">
            <thead>
              <tr>
                <th className="border border-gray-300 px-4 py-2">Metric</th>
                <th className="border border-gray-300 px-4 py-2">Language</th>
                <th className="border border-gray-300 px-4 py-2">Value</th>
              </tr>
            </thead>
            <tbody>
              {resultData.map(({ metric, language, value }) => (
                <tr key={`${metric}-${language}`}>
                  <td className="border border-gray-300 px-4 py-2">{metric}</td>
                  <td className="border border-gray-300 px-4 py-2">{language}</td>
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
