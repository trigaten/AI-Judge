#include <bits/stdc++.h>
#include "include/rapidjson/document.h"
#include "include/rapidjson/prettywriter.h" 
#include "include/rapidjson/ostreamwrapper.h"
#include "include/rapidjson/writer.h"
#include "include/rapidjson/filewritestream.h"
#include <fstream>

using namespace rapidjson;

int main(int argc, char **argv) {

    if (argc < 2) {
        std::cerr << "Missing comments filename.\n";
        exit(1);
    }

    std::ifstream readfile(argv[1]);

    if (readfile.fail()) {
        std::cerr << "File does not exist.\n";
        exit(1);
    }

    FILE *out_f = fopen("parsedposts.json", "w");

    auto buffer = std::make_unique<std::array<char, 4096>>();

    FileWriteStream fws(out_f, buffer.get()->data(), 4096);

    std::string line;

    fws.Put('[');

    size_t processed_so_far = 0;
    size_t parsed_so_far = 0;
    while (std::getline(readfile, line)) {
        rapidjson::Document unparsed;
        
        if (unparsed.Parse(line.c_str()).HasParseError()) {
            std::cout << "Error parsing line to JSON." << std::endl;
            continue;
        }

        auto subreddit = unparsed["subreddit"].GetString();
        auto body = unparsed["selftext"].GetString();

        processed_so_far++;

        if (processed_so_far % 1000000 == 0) {
            std::cerr << "Parsed " << parsed_so_far << " so far. (Processed " << processed_so_far << ")\n";
        }

        if (strcmp(subreddit, "AmItheAsshole") != 0 ||
            strcmp(body, "[deleted]") == 0 ||
            strcmp(body, "[removed]") == 0) {
            continue;
        }

        parsed_so_far++;

        rapidjson::Document parsed;
        auto alloc = parsed.GetAllocator();

        parsed.SetObject();

        parsed.AddMember("id", unparsed["id"], alloc);
        parsed.AddMember("title", unparsed["title"], alloc);
        parsed.AddMember("body", unparsed["selftext"], alloc);
        parsed.AddMember("score", unparsed["score"], alloc);

        rapidjson::Writer<rapidjson::FileWriteStream> writer(fws);
        parsed.Accept(writer);
        
        fws.Put(',');
        fws.Put('\n');

        if (parsed_so_far % 300 == 0) {
            fws.Flush();
        }
    }

    fws.Put(']');
    fws.Flush();

    fclose(out_f);

    std::cerr << "Done.\n";

    return 0;
}
