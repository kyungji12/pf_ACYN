import React from 'react';
import PropTypes from "prop-types";

function Food({name, picture, rating}) {
  return <div>
    <h1>I like {name}</h1>
    <h4>{rating}/5</h4>
    <img src={picture} alt={name} />
  </div>
}

Food.propTypes = {
  name: PropTypes.string.isRequired,
  picture: PropTypes.string.isRequired,
  rating: PropTypes.number.isRequired
};

const foodILike =[
  {
    id : 1,
    name : "kimchi",
    image : "https://www.maangchi.com/wp-content/uploads/2019/11/vegankimchi-insta.jpg",
    rating: 4.3,
  },
  {
    id : 2,
    name : "samgiopsal",
    image : "https://www.koreanbapsang.com/wp-content/uploads/2012/05/DSC_1910-e1499143384126.jpg",
    rating: 4.8,
  },
  {
    id : 3,
    name : "chukumi",
    image : "http://1.bp.blogspot.com/-fTtgX7TpwZ0/VGwBSy7jkuI/AAAAAAAAIiQ/tB9f6DzV2Y4/s1600/4.jpg",
    rating: 4.5,
  }
];

function App() {
  return (
    <div >
      {foodILike.map(dish => 
        <Food 
        key={dish.id}
        name={dish.name}
        picture={dish.image}
        rating={dish.rating}
        />
        )}
    </div>
  );
}

export default App;
