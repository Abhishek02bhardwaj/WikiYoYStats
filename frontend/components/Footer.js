import Image from 'next/image';
import footerData from '../content/footer.json';

export default function Footer() {
  return (
    <footer className="bg-gray_footer text-gray-200 py-8">
      <div className="container md:mx-auto">
        <div className="flex flex-col md:flex-row justify-between">
          <div className="flex flex-col md:flex-row items-center">
            <div className="mb-4 mx-5 md:mb-0">
              <Image src="/logo.svg" alt="Wikimedia YoY Statistics" width={70} height={15} />
            </div>

            {/*
            <div className="grid grid-cols-1 md:grid-cols-2 gap-2 mt-2">
              <div className="place-self-center">
                <label className="block text-sm mb-2">Choose your preferred language:</label>
              </div>
              <div className="place-self-center">
                <select className="p-2 rounded-md text-gray-800">
                  {footerData.languages.map((language) => (
                    <option key={language.value} value={language.value}>
                      {language.label}
                    </option>
                  ))}
                </select>
              </div>
            </div> */}
          </div>

          <div className="grid grid-cols-2 sm-custom:grid-cols-3 gap-4 place-items-center text-sm mt-6 md:mt-0">
            {footerData.sections.map((section, index) => (
              <div key={index} className={index === 2 ? 'place-self-center ml-0 col-span-2 sm-custom:col-span-1' : 'ml-3'}>
                <h4 className="font-semibold mb-2">{section.title}</h4>
                <ul>
                  {section.links.map((link, idx) => (
                    <li key={idx}>
                      <a href={link.url} className="hover:underline">
                        {link.label}
                      </a>
                    </li>
                  ))}
                </ul>
              </div>
            ))}
          </div>
        </div>

        <div className="text-center text-sm mt-6">
          <p>
            All data, charts, and other content is available under the{' '}
            <a href="#" className="text-blue-400 hover:underline">
              Creative Commons CC0 dedication
            </a>
            .
          </p>
        </div>
      </div>
    </footer>
  );
}
