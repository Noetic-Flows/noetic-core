'use client';

import { EngineProvider, useEngine } from '../components/EngineProvider';
import { ReadyState } from 'react-use-websocket';

function HubInterface() {
  const { readyState, lastUI, sendIntent, rawMessage } = useEngine();

  const connectionStatus = {
    [ReadyState.CONNECTING]: 'Connecting',
    [ReadyState.OPEN]: 'Open',
    [ReadyState.CLOSING]: 'Closing',
    [ReadyState.CLOSED]: 'Closed',
    [ReadyState.UNINSTANTIATED]: 'Uninstantiated',
  }[readyState];

  return (
    <main className="flex min-h-screen flex-col items-center justify-between p-24 bg-slate-950 text-white">
      <div className="z-10 w-full max-w-5xl items-center justify-between font-mono text-sm lg:flex">
        <p className="fixed left-0 top-0 flex w-full justify-center border-b border-gray-300 bg-gradient-to-b from-zinc-200 pb-6 pt-8 backdrop-blur-2xl dark:border-neutral-800 dark:bg-zinc-800/30 dark:from-inherit lg:static lg:w-auto  lg:rounded-xl lg:border lg:bg-gray-200 lg:p-4 lg:dark:bg-zinc-800/30">
          Noetic Hub&nbsp;
          <code className="font-bold">v0.1</code>
        </p>
        <div className="fixed bottom-0 left-0 flex h-48 w-full items-end justify-center bg-gradient-to-t from-white via-white dark:from-black dark:via-black lg:static lg:h-auto lg:w-auto lg:bg-none">
          Status: {connectionStatus}
        </div>
      </div>

      <div className="relative flex place-items-center">
        {lastUI ? (
          <div className="w-full max-w-3xl p-4 bg-gray-800 rounded-lg shadow-xl">
            <h2 className="text-xl font-bold mb-4">ASP Render</h2>
            <pre className="text-xs bg-black p-4 rounded overflow-auto max-h-[500px]">
              {JSON.stringify(lastUI, null, 2)}
            </pre>
          </div>
        ) : (
          <div className="text-center">
            <h1 className="text-2xl font-bold mb-4">Waiting for Engine Stream...</h1>
            <div className="animate-pulse bg-gray-700 h-4 w-64 rounded mx-auto"></div>
          </div>
        )}
      </div>

      {/* Debug Section */}
      <div className="w-full max-w-5xl mt-8 border-t border-gray-700 pt-8">
        <h3 className="text-lg font-bold mb-2">Debug Console</h3>
        <div className="grid grid-cols-2 gap-4">
          <div className="bg-black p-4 rounded text-xs overflow-auto max-h-40">
            <p className="font-bold text-gray-400 mb-1">Last Raw Message:</p>
            <div className="whitespace-pre-wrap font-mono text-green-400">
              {rawMessage || "No messages received"}
            </div>
          </div>
          <div className="flex flex-col gap-2">
            <button
              onClick={() => sendIntent({ name: "ping" })}
              className="p-3 bg-blue-600 rounded hover:bg-blue-700 transition font-bold"
            >
              Ping -&gt;
            </button>
          </div>
        </div>
      </div>
    </main>
  );
}

export default function Home() {
  return (
    <EngineProvider>
      <HubInterface />
    </EngineProvider>
  )
}
