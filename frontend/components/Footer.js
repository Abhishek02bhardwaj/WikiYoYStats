import footerData from '../content/footer.json';

export default function Footer() {
  return (
    <footer className="bg-gray_footer text-gray-200 py-8">
      <div className="container md:mx-auto">
        <div className="flex flex-col  justify-between">

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
      </div>
    </footer>
  );
}
