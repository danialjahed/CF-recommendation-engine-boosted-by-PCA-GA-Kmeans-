//this is query find top rated movie written by me and my best firend elyas|github.com/elyas74
db.top_rated_movie.drop();
db.getCollection('rates').aggregate([{
        $match: {}
    }, {
        $project: {
            _id: 0,
            movie_rate: 1,
            user_id: 1
        }
    }, {
        $unwind: "$movie_rate"
    }, {
        "$match": {
            "movie_rate.rate": {
                $ne: parseInt("NaN")
            }
        }
    }, {
        $group: {
            _id: "$movie_rate.movie_id",
            avg_r: {
                $avg: "$movie_rate.rate"
            },
            count_v: {
                $sum: 1
            }
        }
    },
    // sort
    {
        $out: "top_rated_movie"
    }

]);

// dalghak 2 generator
// db.getCollection('dalghak').aggregate([{
//         $group: {
//             _id: "1",
//
//             C: {
//                 $avg: "$avg_r"
//             },
//             M: {
//                 $avg: "$count_v"
//             }
//         }
//     }, // out to db
//     {
//         $out: "dalghak2"
//     }
// ]);
