import React, { createContext, useContext, useState, ReactNode } from "react";

// Define Disease type and Context structure
type Disease = {
    id: string;
    Name: string;
    Overview?: string;
    vector?: any; // Optional field if used for relevance feedback
};

interface AppContextType {
    diseases: Disease[];
    setDiseases: React.Dispatch<React.SetStateAction<Disease[]>>;
    selectedDiseases: string[];
    setSelectedDiseases: React.Dispatch<React.SetStateAction<string[]>>;
    lastInputValue: string;
    setLastInputValue: React.Dispatch<React.SetStateAction<string>>;
    inputValue: string;
    setInputValue: React.Dispatch<React.SetStateAction<string>>;
}

const AppContext = createContext<AppContextType | undefined>(undefined);

// AppProvider component
export const AppProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
    const [diseases, setDiseases] = useState<Disease[]>([]);
    const [selectedDiseases, setSelectedDiseases] = useState<string[]>([]);
    const [lastInputValue, setLastInputValue] = useState<string>("");
    const [inputValue, setInputValue] = useState<string>("");

    return (
        <AppContext.Provider
            value={{
                diseases,
                setDiseases,
                selectedDiseases,
                setSelectedDiseases,
                lastInputValue,
                setLastInputValue,
                inputValue,
                setInputValue,
            }}
        >
            {children}
        </AppContext.Provider>
    );
};

// Hook to use the AppContext
export const useAppContext = (): AppContextType => {
    const context = useContext(AppContext);
    if (!context) {
        throw new Error("useAppContext must be used within an AppProvider");
    }
    return context;
};

