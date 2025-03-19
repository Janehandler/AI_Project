import SwiftUI
import Foundation

@main
struct AIMacAssistantApp: App {
    var body: some Scene {
        WindowGroup {
            ContentView()
        }
    }
}

struct ContentView: View {
    @State private var userInput: String = ""
    @State private var chatLog: [String] = []
    let commandsFilePath = FileManager.default.homeDirectoryForCurrentUser
        .appendingPathComponent("Documents/AIAssistant/commands.txt").path
    let logsFilePath = FileManager.default.homeDirectoryForCurrentUser
        .appendingPathComponent("Documents/AIAssistant/logs.txt").path
    
    var body: some View {
        VStack {
            ScrollView {
                ForEach(chatLog, id: \.self) { msg in
                    Text(msg).padding(.bottom, 2)
                }
            }
            .frame(maxWidth: .infinity, maxHeight: .infinity)
            HStack {
                TextField("Type command or question...", text: $userInput)
                    .textFieldStyle(RoundedBorderTextFieldStyle())
                    .frame(minHeight: 30)
                Button("Send") {
                    let t = userInput.trimmingCharacters(in: .whitespacesAndNewlines)
                    guard !t.isEmpty else { return }
                    logCommandToFile(t)
                    chatLog.append("User: \(t)")
                    sendToOpenAI(userMessage: t)
                    userInput = ""
                }
            }
            .padding()
            HStack {
                Button("Grant Max Permissions") {
                    requestAccessibilityPermissions()
                    DispatchQueue.main.asyncAfter(deadline: .now() + 2) {
                        requestFullDiskAccessPermissions()
                    }
                }
                Button("Grant More Permissions") {
                    requestCameraPermissions()
                    DispatchQueue.main.asyncAfter(deadline: .now() + 2) {
                        requestMicrophonePermissions()
                    }
                    DispatchQueue.main.asyncAfter(deadline: .now() + 4) {
                        requestScreenRecordingPermissions()
                    }
                }
            }
        }
        .padding()
        .onAppear {
            createDirectoryIfNeeded()
            createFileIfNeeded(path: commandsFilePath)
            createFileIfNeeded(path: logsFilePath)
        }
    }
    
    func sendToOpenAI(userMessage: String) {
        let openAIAPIKey = "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"
        guard let url = URL(string: "https://api.openai.com/v1/chat/completions") else {
            appendToChatLog("Error: Invalid OpenAI URL.")
            return
        }
        let systemRole = "You are an AI controlling macOS. Use SYSTEM: for shell or AppleScript, READFILE <path> or WRITEFILE <path> <content> for file ops, RUNPY: /path/to/script.py <args> for Python, or other expansions. Otherwise, answer normally."
        let messages: [[String: String]] = [
            ["role": "system", "content": systemRole],
            ["role": "user", "content": userMessage]
        ]
        let requestBody: [String: Any] = ["model": "gpt-3.5-turbo", "messages": messages]
        let jsonData = try? JSONSerialization.data(withJSONObject: requestBody)
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.addValue("Bearer \(openAIAPIKey)", forHTTPHeaderField: "Authorization")
        request.addValue("application/json", forHTTPHeaderField: "Content-Type")
        request.httpBody = jsonData
        URLSession.shared.dataTask(with: request) { d, r, e in
            if let e = e {
                DispatchQueue.main.async { appendToChatLog("Error calling OpenAI: \(e.localizedDescription)") }
                return
            }
            guard let d = d else {
                DispatchQueue.main.async { appendToChatLog("Error: No data from OpenAI.") }
                return
            }
            do {
                if let j = try JSONSerialization.jsonObject(with: d) as? [String: Any],
                   let c = j["choices"] as? [[String: Any]],
                   let m = c.first?["message"] as? [String: Any],
                   let con = m["content"] as? String {
                    DispatchQueue.main.async {
                        appendToChatLog("AI: \(con)")
                        handleAiResponse(con)
                    }
                } else {
                    DispatchQueue.main.async { appendToChatLog("Error: Could not parse OpenAI response.") }
                }
            } catch {
                DispatchQueue.main.async { appendToChatLog("Error parsing JSON: \(error.localizedDescription)") }
            }
        }.resume()
    }
    
    func handleAiResponse(_ response: String) {
        if let c = parseSystemCommand(from: response) {
            logEventToFile("AI: Executing \"\(c)\"")
            executeSystemCommand(c)
            appendToChatLog("AI: Executed \"\(c)\"")
        } else if let (path, _) = parseReadFile(from: response) {
            logEventToFile("AI: Reading file \(path)")
            readFile(at: path)
        } else if let (path, content) = parseWriteFile(from: response) {
            logEventToFile("AI: Writing file \(path)")
            writeFile(path: path, content: content)
        } else if let (scriptPath, args) = parseRunPython(from: response) {
            logEventToFile("AI: Running Python script \(scriptPath) with args \(args)")
            runPythonScript(scriptPath, arguments: args)
        }
    }
    
    func parseSystemCommand(from response: String) -> String? {
        let pattern = #"(?i)SYSTEM:\s*(.*)"#
        if let regex = try? NSRegularExpression(pattern: pattern, options: []) {
            let nsrange = NSRange(response.startIndex..<response.endIndex, in: response)
            if let match = regex.firstMatch(in: response, options: [], range: nsrange) {
                if let range1 = Range(match.range(at: 1), in: response) {
                    return String(response[range1]).trimmingCharacters(in: .whitespacesAndNewlines)
                }
            }
        }
        return nil
    }
    
    func parseReadFile(from response: String) -> (String, String)? {
        let pattern = #"(?i)\bREADFILE\s+(.+)"#
        if let regex = try? NSRegularExpression(pattern: pattern, options: []) {
            let nsrange = NSRange(response.startIndex..<response.endIndex, in: response)
            if let match = regex.firstMatch(in: response, options: [], range: nsrange) {
                if let range1 = Range(match.range(at: 1), in: response) {
                    let p = String(response[range1]).trimmingCharacters(in: .whitespacesAndNewlines)
                    return (p, "read")
                }
            }
        }
        return nil
    }
    
    func parseWriteFile(from response: String) -> (String, String)? {
        let pattern = #"(?i)\bWRITEFILE\s+(\S+)\s+(.*)"#
        if let regex = try? NSRegularExpression(pattern: pattern, options: []) {
            let nsrange = NSRange(response.startIndex..<response.endIndex, in: response)
            if let match = regex.firstMatch(in: response, options: [], range: nsrange) {
                if let pathRange = Range(match.range(at: 1), in: response),
                   let contentRange = Range(match.range(at: 2), in: response) {
                    let p = String(response[pathRange]).trimmingCharacters(in: .whitespacesAndNewlines)
                    let c = String(response[contentRange]).trimmingCharacters(in: .whitespacesAndNewlines)
                    return (p, c)
                }
            }
        }
        return nil
    }
    
    func parseRunPython(from response: String) -> (String, [String])? {
        let pattern = #"(?i)\bRUNPY:\s+(\S+)(.*)"#
        if let regex = try? NSRegularExpression(pattern: pattern, options: []) {
            let nsrange = NSRange(response.startIndex..<response.endIndex, in: response)
            if let match = regex.firstMatch(in: response, options: [], range: nsrange) {
                if let scriptRange = Range(match.range(at: 1), in: response),
                   let argsRange = Range(match.range(at: 2), in: response) {
                    let scriptPath = String(response[scriptRange]).trimmingCharacters(in: .whitespacesAndNewlines)
                    let rawArgs = String(response[argsRange]).trimmingCharacters(in: .whitespacesAndNewlines)
                    let arr = rawArgs.components(separatedBy: " ").filter { !$0.isEmpty }
                    return (scriptPath, arr)
                }
            }
        }
        return nil
    }
    
    func executeSystemCommand(_ command: String) {
        if command.hasPrefix("osascript") || command.hasPrefix("tell application") {
            runAppleScriptCommand(command)
        } else {
            runShellCommand(command)
        }
    }
    
    func runShellCommand(_ cmd: String) {
        let task = Process()
        task.executableURL = URL(fileURLWithPath: "/bin/zsh")
        task.arguments = ["-c", cmd]
        do {
            try task.run()
            task.waitUntilExit()
        } catch {
            appendToChatLog("Error running shell command: \(error)")
        }
    }
    
    func runAppleScriptCommand(_ script: String) {
        let full = "osascript -e '\(script)'"
        runShellCommand(full)
    }
    
    func runPythonScript(_ path: String, arguments: [String]) {
        let task = Process()
        task.executableURL = URL(fileURLWithPath: "/usr/bin/python3")
        task.arguments = [path] + arguments
        let pipe = Pipe()
        task.standardOutput = pipe
        task.standardError = pipe
        do {
            try task.run()
            task.waitUntilExit()
            let data = pipe.fileHandleForReading.readDataToEndOfFile()
            if let output = String(data: data, encoding: .utf8), !output.isEmpty {
                appendToChatLog("Python Output:\n\(output)")
            }
        } catch {
            appendToChatLog("Error running Python script: \(error)")
        }
    }
    
    func readFile(at path: String) {
        do {
            let contents = try String(contentsOfFile: path)
            appendToChatLog("File Contents of \(path):\n\(contents)")
        } catch {
            appendToChatLog("Error reading file at \(path): \(error)")
        }
    }
    
    func writeFile(path: String, content: String) {
        do {
            try content.write(toFile: path, atomically: true, encoding: .utf8)
            appendToChatLog("Wrote to file at \(path).")
        } catch {
            appendToChatLog("Error writing file at \(path): \(error)")
        }
    }
    
    func createDirectoryIfNeeded() {
        let folderPath = FileManager.default.homeDirectoryForCurrentUser
            .appendingPathComponent("Documents/AIAssistant")
        if !FileManager.default.fileExists(atPath: folderPath.path) {
            try? FileManager.default.createDirectory(at: folderPath, withIntermediateDirectories: true, attributes: nil)
        }
    }
    
    func createFileIfNeeded(path: String) {
        if !FileManager.default.fileExists(atPath: path) {
            FileManager.default.createFile(atPath: path, contents: nil, attributes: nil)
        }
    }
    
    func logCommandToFile(_ command: String) {
        let t = formattedCurrentDate()
        let entry = "[\(t)] User Command: \(command)\n"
        writeToFile(filePath: commandsFilePath, content: entry)
        let logEntry = "[\(t)] User: \(command)\n"
        writeToFile(filePath: logsFilePath, content: logEntry)
    }
    
    func logEventToFile(_ event: String) {
        let t = formattedCurrentDate()
        let entry = "[\(t)] \(event)\n"
        writeToFile(filePath: logsFilePath, content: entry)
    }
    
    func writeToFile(filePath: String, content: String) {
        if let fh = FileHandle(forWritingAtPath: filePath) {
            fh.seekToEndOfFile()
            if let d = content.data(using: .utf8) {
                fh.write(d)
            }
            fh.closeFile()
        }
    }
    
    func appendToChatLog(_ text: String) {
        chatLog.append(text)
    }
    
    func formattedCurrentDate() -> String {
        let f = DateFormatter()
        f.dateFormat = "yyyy-MM-dd HH:mm:ss"
        return f.string(from: Date())
    }
    
    func requestAccessibilityPermissions() {
        let s = """
        tell application "System Settings"
            activate
            reveal anchor "Privacy_Accessibility" of pane id "com.apple.preference.security"
        end tell
        """
        runAppleScriptCommand(s)
    }
    
    func requestFullDiskAccessPermissions() {
        let s = """
        tell application "System Settings"
            activate
            reveal anchor "Privacy_AllFiles" of pane id "com.apple.preference.security"
        end tell
        """
        runAppleScriptCommand(s)
    }
    
    func requestCameraPermissions() {
        let s = """
        tell application "System Settings"
            activate
            reveal anchor "Privacy_Camera" of pane id "com.apple.preference.security"
        end tell
        """
        runAppleScriptCommand(s)
    }
    
    func requestMicrophonePermissions() {
        let s = """
        tell application "System Settings"
            activate
            reveal anchor "Privacy_Microphone" of pane id "com.apple.preference.security"
        end tell
        """
        runAppleScriptCommand(s)
    }
    
    func requestScreenRecordingPermissions() {
        let s = """
        tell application "System Settings"
            activate
            reveal anchor "Privacy_ScreenCapture" of pane id "com.apple.preference.security"
        end tell
        """
        runAppleScriptCommand(s)
    }
}
