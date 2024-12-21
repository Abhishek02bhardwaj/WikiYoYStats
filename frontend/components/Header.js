import Image from "next/image";

export default function Header() {
  return (
    <header className="bg-white shadow">
      <div className="container mx-auto flex items-center justify-between py-4">
        <div className="justify-between mx-auto">
          <div className="flex items-center self-center justify-self-end mr-4">
          <Image src="/logo.svg" alt="Wikimedia YoY Statistics" width={50} height={10} />
            <h1 className="text-2xl ml-5 font-semibold text-gray-700">
              Wikimedia YoY Growth
            </h1>
          </div>

        </div>
      </div>
    </header>
  );
}
