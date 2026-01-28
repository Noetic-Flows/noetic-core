'use client';

import React, { createContext, useContext, useEffect, useState } from 'react';
import useWebSocket, { ReadyState } from 'react-use-websocket';

type EngineContextType = {
    readyState: ReadyState;
    sendIntent: (payload: any) => void;
    lastUI: any; // The latest UI tree received from the engine
    rawMessage: string | null;
};

const EngineContext = createContext<EngineContextType>({
    readyState: ReadyState.UNINSTANTIATED,
    sendIntent: () => { },
    lastUI: null,
    rawMessage: null,
});

export const useEngine = () => useContext(EngineContext);

export const EngineProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
    const [lastUI, setLastUI] = useState<any>(null);
    const [rawMessage, setRawMessage] = useState<string | null>(null);

    // Connect to Local Engine
    const { sendMessage, lastMessage, readyState } = useWebSocket('ws://localhost:8000/ws/asp', {
        shouldReconnect: () => true,
        filter: () => true, // Receive all messages (was FALSE previously, blocking everything)
        onOpen: () => console.log('WS Open'),
        onClose: () => console.log('WS Closed'),
        onError: (e) => console.error('WS Error', e),
    });

    // Handle Incoming Messages
    useEffect(() => {
        if (lastMessage !== null) {
            console.log("WS Message Received:", lastMessage.data);
            setRawMessage(lastMessage.data);
            try {
                const data = JSON.parse(lastMessage.data);
                if (data.type === 'STATE_UPDATE') {
                    // Update local UI state
                    if (data.payload && data.payload.ui) {
                        console.log("Setting UI State:", data.payload.ui);
                        setLastUI(data.payload.ui);
                    }
                }
            } catch (e) {
                console.error("Failed to parse ASP message", e);
            }
        }
    }, [lastMessage]);

    // Initial Connect Handshake
    useEffect(() => {
        if (readyState === ReadyState.OPEN) {
            sendMessage(JSON.stringify({
                type: "CONNECT",
                client_id: "web-hub",
                version: "1.0"
            }));
        }
    }, [readyState, sendMessage]);

    const sendIntent = (payload: any) => {
        sendMessage(JSON.stringify({
            type: "INTENT",
            payload,
            ref_id: crypto.randomUUID()
        }));
    };

    return (
        <EngineContext.Provider value={{ readyState, sendIntent, lastUI, rawMessage }}>
            {children}
        </EngineContext.Provider>
    );
};
