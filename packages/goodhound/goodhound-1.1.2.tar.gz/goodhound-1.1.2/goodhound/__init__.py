import argparse
from os import getcwd
from sys import exit
import logging
from datetime import datetime
from goodhound import ghresults, sqldb, ghutils, paths, neodb

def arguments():
    argparser = argparse.ArgumentParser(description="BloodHound Wrapper to determine the Busiest Attack Paths to High Value targets.", add_help=True, epilog="Attackers think in graphs, Defenders think in actions, Management think in charts.")
    parsegroupdb = argparser.add_argument_group('Neo4jConnection')
    parsegroupdb.add_argument("-u", "--username", default="neo4j", help="Neo4j Database Username (Default: neo4j)", type=str)
    parsegroupdb.add_argument("-p", "--password", default="neo4j", help="Neo4j Database Password (Default: neo4j)", type=str)
    parsegroupdb.add_argument("-s", "--server", default="bolt://localhost:7687", help="Neo4j server Default: bolt://localhost:7687)", type=str)
    parsegroupoutput = argparser.add_argument_group('Output Formats')
    parsegroupoutput.add_argument("-o", "--output-format", default="csv", help="Output formats supported: stdout, csv, md (markdown). Default: csv.", type=str, choices=["stdout", "csv", "md", "markdown"])
    parsegroupoutput.add_argument("-d", "--output-dir", default=getcwd(), help="Directory to save the output. Defaults to current directory.", type=str)
    parsegroupoutput.add_argument("-q", "--quiet", help="Mutes all output.", action="store_true")
    parsegroupoutput.add_argument("-v", "--verbose", help="Enables informational output.", action="store_true")
    parsegroupoutput.add_argument("--debug", help="Enables debug logging.", action="store_true")
    parsegroupqueryparams = argparser.add_argument_group('Query Parameters')
    parsegroupqueryparams.add_argument("-r", "--results", default="5", help="The number of busiest paths and weakest links to output. Default: 5", type=int)
    parsegroupqueryparams.add_argument("-sort", "--sort", default="risk", help="Option to sort results by number of users with the path, number of hops or risk score. Default: Risk Score", type=str, choices=["users", "hops", "risk"])
    parsegroupschema = argparser.add_argument_group('Schema')
    parsegroupschema.add_argument("-sch", "--schema", help="Optionally select a text file containing custom cypher queries to add labels to the neo4j database. e.g. Use this if you want to add the highvalue label to assets that do not have this by default in the BloodHound schema.", type=str)
    parsegroupschema.add_argument("--patch41", help="A temporary option to patch a bug in Bloodhound 4.1 relating to the highvalue attribute.", action="store_true")
    parsegroupsql = argparser.add_argument_group('SQLite Database')
    parsegroupsql.add_argument("--db-skip", help="Skips the logging of attack paths to a local SQLite Database", action="store_true")
    parsegroupsql.add_argument("-sqlpath", "--sql-path", default=getcwd(), help="Sets the file path of the GoodHound Database file", type=str)
    args = argparser.parse_args()
    return args

def main():
    args = arguments()
    if args.quiet:
        logging.basicConfig(level=logging.CRITICAL)
    elif args.debug:
        logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
    elif args.verbose:
        logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)
    ghutils.checkoutdir(args.output_dir)
    if not args.quiet:    
        ghutils.banner()
    graph = neodb.db_connect(args)
    starttime = datetime.now()
    neodb.warmupdb(graph, args)
    if args.schema:
        neodb.schema(graph, args)
    neodb.cost(graph)
    if args.patch41:
        neodb.bloodhound41patch(graph)
    neodb.set_hv_for_dcsyncers(graph)
    groupswithpath, userswithpath = paths.shortestgrouppath(graph, starttime, args)
    totalenablednonadminusers = neodb.totalusers(graph)
    uniquegroupswithpath = paths.getuniquegroupswithpath(groupswithpath)
    groupswithmembers = paths.processgroups(graph, uniquegroupswithpath, args)
    totaluniqueuserswithpath = paths.gettotaluniqueuserswithpath(groupswithmembers, userswithpath)
    results = ghresults.generateresults(groupswithpath, groupswithmembers, totalenablednonadminusers, userswithpath)
    new_path, seen_before, scandatenice = sqldb.db(results, graph, args)
    uniqueresults = ghresults.getuniqueresults(results)
    top_results = ghresults.sortresults(args, uniqueresults)
    totalpaths = len(groupswithpath+userswithpath)
    weakest_links = paths.weakestlinks(groupswithpath, totalpaths, userswithpath, args)
    grandtotalsdf, weakest_linkdf, busiestpathsdf = ghresults.grandtotals(totaluniqueuserswithpath, totalenablednonadminusers, totalpaths, new_path, seen_before, weakest_links, top_results)
    ghresults.output(args, grandtotalsdf, weakest_linkdf, busiestpathsdf, scandatenice, starttime)

if __name__ == "__main__":
    main()