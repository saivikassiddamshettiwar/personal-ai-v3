from ddgs import DDGS


def search_web(

    query,

    max_results=5

):

    try:

        with DDGS() as ddgs:

            results = list(

                ddgs.text(

                    query,

                    max_results=max_results

                )

            )

        return results

    except Exception as error:

        print(
            "Web search error:",
            error
        )

        return []