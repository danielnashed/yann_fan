import Button from './Button.js';
export default function TextInput({ content, onChange, onKeyDown, className}) {
    return (
        <div className="relative w-4/5 mx-auto">
            <textarea 
                value={content} 
                onChange={onChange}
                onKeyDown={onKeyDown}
                className={className}
                placeholder="Type your message..."
            />
            <div className="absolute right-0 bottom-0">
                <Button 
                    content="^" 
                    onClick={onChange} 
                />
            </div>
        </div>
    );
  }