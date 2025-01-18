import { useState } from "react";
import { Document, Page, pdfjs } from "react-pdf";
import 'react-pdf/dist/esm/Page/AnnotationLayer.css';
import 'react-pdf/dist/esm/Page/TextLayer.css';

pdfjs.GlobalWorkerOptions.workerSrc = '/pdf.worker.min.mjs';

export default function Modal() {  
    const [uploadedFiles, setUploadedFiles] = useState([]);

    const handleFileUpload = (event) => {
        const files = Array.from(event.target.files);
        const filesWithPreviews = files.map((file) => ({
            file,
            type: file.type,
            preview: file.type.startsWith("image/") ? URL.createObjectURL(file) : null,
        }));
        setUploadedFiles((prevFiles) => [...prevFiles, ...filesWithPreviews]);
    };

    return (
        <dialog id="my_modal_3" className="modal">
            <div className="modal-box w-11/12 max-w-5xl h-[80vh] p-6 bg-neutral-800/100 shadow-2xl shadow-black flex flex-col">
                <form method="dialog">
                    <button className="btn btn-sm btn-circle btn-ghost absolute right-2 top-2">
                        ✕
                    </button>
                </form>
                <h3 className="font-normal text-lg font-['Montserrat'] mb-4">
                    Documents uploaded in the past live here.
                </h3>
                {/* File Upload Input */}
                <div className="mb-4 flex justify-center">
                    <label
                        htmlFor="file-upload"
                        className="btn bg-neutral-600 text-white px-4 py-2 cursor-pointer font-['Montserrat']">
                        Upload Files
                    </label>
                    <input
                        id="file-upload"
                        type="file"
                        multiple
                        accept=".png,.jpg,.jpeg,.pdf,.doc,.docx"
                        className="hidden"
                        onChange={handleFileUpload}
                    />
                </div>
                {/* Uploaded Files Grid */}
                <div className="overflow-y-auto h-full bg-neutral-900/50 p-4 rounded-md">
                    {uploadedFiles.length > 0 ? (
                        <div className="grid grid-cols-3 gap-4">
                            {uploadedFiles.map((fileObj, index) => (
                                <div
                                    key={index}
                                    className="bg-neutral-700 text-white p-2 rounded-md flex flex-col items-center text-sm break-words"
                                >
                                    {fileObj.type.startsWith("image/") ? (
                                        <img
                                            src={fileObj.preview}
                                            alt={fileObj.file.name}
                                            className="w-full h-32 object-cover rounded-md mb-2"
                                        />
                                    ) : fileObj.type === "application/pdf" ? (
                                        <div className="w-full h-32 bg-neutral-600 flex items-center justify-center text-neutral-300 rounded-md mb-2 overflow-hidden">
                                            <Document
                                                file={fileObj.file}
                                                className="w-full h-full"
                                            >
                                                <Page pageNumber={1} scale={0.8} />
                                            </Document>
                                        </div>
                                    ) : (
                                        <div className="w-full h-32 bg-neutral-600 flex items-center justify-center text-neutral-300 rounded-md mb-2">
                                            File Preview Unavailable
                                        </div>
                                    )}
                                    <span className="truncate text-center">
                                        {fileObj.file.name}
                                    </span>
                                </div>
                            ))}
                        </div>
                    ) : (
                        <p className="text-neutral-400 text-center">
                            No files uploaded yet.
                        </p>
                    )}
                </div>
            </div>
        </dialog>
    );
}